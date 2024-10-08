import logging
import typing as tp
import aioboto3
from datetime import datetime
import pytz
from enum import Enum
import asyncio

from ..tg import BaseTgClient, S3Manager, AuthorizeRedisClient, SessionRedisClient
from ..db import PGClient, Chat_info
from ..config import Config
from .. import schema as schema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SessionActivity(Enum):
    DENIED = "denied"
    SPAM = "spam"
    WITH_HISTORY = "WITH_HISTORY"
    ORDINARY = "ordinary"
    CHECK_ACCESS = "check_access"


class OperationsController:
    BUCKET_NAME = "igorkopylov"

    def __init__(
        self,
        tg_base_client: BaseTgClient,
        s3client: S3Manager,
        session_redis_client: SessionRedisClient,
        authorize_redis_client: AuthorizeRedisClient,
        pg_client: PGClient,
    ):
        self.tg_base_client = tg_base_client
        self.s3client = s3client
        self.session = aioboto3.Session(
            aws_access_key_id=Config.YANDEX_KEY_ID,
            aws_secret_access_key=Config.YANDEX_KEY_SECRET
        )
        self.session_redis_client = session_redis_client
        self.authorize_redis_client = authorize_redis_client
        self.moscow_tz = pytz.timezone(Config.TIMEZONE)
        self.pg_client = pg_client
    
    async def bad_response(self, chat_id: int, user_name: str) -> str:
        await self.tg_base_client.send_chat_action(chat_id=chat_id, action='typing')
        try:
            await self.tg_base_client.process_bad_request(chat_id, user_name)
        except Exception as e:
            raise e
        return "ok"
    
    async def _get_user_info(self, chat_id: str, user_name: str) -> tp.Optional[schema.redis.RedisAuthorize]:
        if not self.authorize_redis_client.check_connection():
            await self.authorize_redis_client.connect()
        user_info: schema.redis.RedisAuthorize = await self.authorize_redis_client.get_value(chat_id)
        logger.info(f"Parsed data from redis {user_info}")
        if user_info is None:
            selected_rows: tp.Optional[list[Chat_info]] = await self.pg_client.get_chat_info(chat_id=chat_id)
            logger.info(f"Parsed info from DB: {selected_rows}")
            if selected_rows:
                selected_user_info = selected_rows[0]
                user_info = schema.redis.RedisAuthorize(
                    chat_id=selected_user_info.chat_id,
                    first_name=selected_user_info.first_name,
                    pay=selected_user_info.pay,
                    date_end=str(selected_user_info.end_date),
                    date_start=str(selected_user_info.start_date),
                )

            else:
                return None
        return user_info


    async def check_access(self, chat_id: str, user_name: str) -> schema.redis.AccessLevel:

        user_info = await self._get_user_info(chat_id=chat_id, user_name=user_name)
        if not user_info:
            return schema.redis.AccessLevel.DENIED
        now = datetime.now(self.moscow_tz)
        access = schema.redis.AccessLevel.DENIED
        
        if not self.session_redis_client.check_connection():
            await self.session_redis_client.connect()

        date2 = datetime.strptime(user_info.date_end, "%Y-%m-%d")
        if (date2.date() - now.date()).days >= 0:
            access = schema.redis.AccessLevel.GRANTED
        else:
            access = schema.redis.AccessLevel.EXPIRED
        
        await self.session_redis_client.set_value(schema.redis.RedisSession(
            chat_id=chat_id,
            first_name=user_name,
            access=access,
            last_session=int(datetime.now().timestamp()),
        ))
        return access == schema.redis.AccessLevel.GRANTED
    
    async def check_last_session(self, future: asyncio.Future, chat_id: str) -> SessionActivity:
        now = int(datetime.now().timestamp())
        if not self.session_redis_client.check_connection():
            await self.session_redis_client.connect()
        user_info: schema.redis.RedisSession = await self.session_redis_client.get_value(chat_id)
        if not user_info:
            future.set_result(SessionActivity.CHECK_ACCESS)
        elif user_info.access != schema.redis.AccessLevel.GRANTED:
            future.set_result(SessionActivity.DENIED)
        elif abs(now - user_info.last_session) <= 5:
            future.set_result(SessionActivity.SPAM)
        elif 5 <= abs(now - user_info.last_session) <= 60 * 2:
            future.set_result(SessionActivity.WITH_HISTORY)
        else:
            future.set_result(SessionActivity.ORDINARY)

    async def _gather(*args):
        return await asyncio.gather(*args, return_exceptions=False)

    async def create_response(self, chat_id: int, message_text: str, user_name: str) -> int:
        loop = asyncio.get_running_loop()
        session_condition_future: asyncio.Future = loop.create_future()
        asyncio.create_task(self.check_last_session(future=session_condition_future, chat_id=str(chat_id)))
        await self.tg_base_client.send_chat_action(chat_id=str(chat_id), action='typing')
        session_condition = await session_condition_future
        logger.info(f"{session_condition_future}, {session_condition}")
        match session_condition:  # TODO: simplify
            case SessionActivity.SPAM:
                logger.info(f"Spamer user: {user_name}, {chat_id}")
                await self.tg_base_client.process_spam_user(chat_id, user_name)
            case SessionActivity.DENIED:
                logger.info(f"An unauthorized user: {user_name}, {chat_id}")
                await self.tg_base_client.process_unauthorized_user(chat_id, user_name)
            case SessionActivity.CHECK_ACCESS:
                access_status = await self.check_access(chat_id=str(chat_id), user_name=user_name)
                if access_status != schema.redis.AccessLevel.GRANTED:
                    logger.info(f"An unauthorized user: {user_name}, {chat_id}")  # TODO: reduce the same code
                    await self.tg_base_client.process_unauthorized_user(chat_id, user_name)
                    await self.session_redis_client.set_value(schema.redis.RedisSession(  # Update unauthorized user session condition
                        chat_id=str(chat_id),
                        first_name=user_name,
                        access=access_status,
                        last_session=int(datetime.now().timestamp())
                    ))
                else:
                    session_condition = SessionActivity.ORDINARY
        if session_condition not in [SessionActivity.WITH_HISTORY, SessionActivity.ORDINARY]:
            return "ok"
        asyncio.create_task(self.session_redis_client.set_value(schema.redis.RedisSession(
                chat_id=str(chat_id),
                first_name=user_name,
                access=schema.redis.AccessLevel.GRANTED,
                last_session=int(datetime.now().timestamp())
            ))
        )
        history = []
        if session_condition == SessionActivity.WITH_HISTORY:  # TODO: add prompt text
            history_content = await self.s3client.read_file(session=self.session, bucket_name=self.BUCKET_NAME, key=str(chat_id))
            if history_content is not None:
                history.extend(history_content)
        history.append({"role": "user", "content": message_text})
        try:
            ai_answer_future: asyncio.Future = loop.create_future()
            await asyncio.gather(
                self.tg_base_client.process_comand(
                    chat_id,
                    history,
                    user_name,
                    future=ai_answer_future
                    ),
                self.s3client.write_file(
                    session=self.session,
                    bucket_name=self.BUCKET_NAME,
                    key=str(chat_id),
                    content=history,
                    future=ai_answer_future)
            )
        except Exception as e:
            raise e  # TODO: processing except
        return "ok"
