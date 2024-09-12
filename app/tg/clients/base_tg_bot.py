import typing as tp
import logging
import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from .base_ai_client import OpenAiClient
from ...config import Config
from ..magazine import Comands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseTgClient:
    ADMIN_CHAT_ID = None
    MAX_MESSAGE_LENGHT = 4096

    def __init__(self, tg_bot_token: str, proxi_api_key: str,):
        self.bot = Bot(token=tg_bot_token)
        self.ai_client = OpenAiClient(proxi_api_key)
        self.ADMIN_CHAT_ID = Config.ADMIN_CHAT_ID
    
    async def send_chat_action(self, chat_id: int, action: str='typing')->None: # TODO: add enum
        try:
            await self.bot.send_chat_action(chat_id=chat_id, action=action)
        except TelegramForbiddenError:
            logger.error(f"blocked by user, chat id: {chat_id}")


    async def process_comand(self, chat_id: int, context: list[dict], user_name: str, *, future: tp.Optional[asyncio.Future] = None) -> None:
        ai_response = await self.ai_client.process_text_message(history=context)
        if future:
            future.set_result(ai_response)
        try:
            # if len(ai_response) > self.MAX_MESSAGE_LENGHT:
            #     left_bound = 0
            #     right_bound = self.MAX_MESSAGE_LENGHT - 100
            #     while True:
                    
            await self.bot.send_message(chat_id, ai_response)
        except TelegramForbiddenError:
            logger.error(f"blocked by @{user_name}, chat id: {chat_id}")
        await self.bot.send_message(self.ADMIN_CHAT_ID, f"User: {user_name}, context: {context}")


    async def process_spam_user(self, chat_id: int, user_name: str) -> None:
        try:
            await self.bot.send_message(chat_id, f"{user_name}, {Comands.spam_message}")
        except TelegramForbiddenError:
            logger.error(f"blocked by @{user_name}, chat id: {chat_id}")
        await self.bot.send_message(self.ADMIN_CHAT_ID, f"Spamer User: @{user_name}, chat_id: {chat_id}")

    async def process_unauthorized_user(self, chat_id: int, user_name: str) -> None:
        try:
            await self.bot.send_message(chat_id, f"{user_name}, {Comands.unauthorized_message}")
        except TelegramForbiddenError:
            logger.error(f"blocked by @{user_name}, chat id: {chat_id}")
        await self.bot.send_message(self.ADMIN_CHAT_ID, f"User: @{user_name}, chat_id: {chat_id}")
    
    async def process_bad_request(self, chat_id: int, user_name: str) -> None:
        try:
            await self.bot.send_message(chat_id, Comands.bad_request_message)
        except:
            await self.bot.send_message(self.ADMIN_CHAT_ID, f"User: @{user_name}, bad_reqest")





# async def get_s3_client():  # TODO: ADD CHAT HISTORY
#     session = aioboto3.Session(
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#     )
#     return session.client('s3')

# async def process_text_message(text, chat_id) -> str:
#     model = "gpt-3.5-turbo"

#     # Чтение текущей истории чата
#     s3client = await get_s3_client()
#     history = []
    
#     try:
#         history_object_response = await s3client.get_object(
#             Bucket=S3_BUCKET_NAME, Key=f"{chat_id}.json"
#         )
#         history = json.loads(await history_object_response["Body"].read())
#     except Exception:
#         pass

#     history.append({"role": "user", "content": text})

#     try:
#         chat_completion = await client.chat.completions.create(
#             model=model, messages=history
#         )
#     except Exception as e:
#         if type(e).__name__ == "BadRequestError":
#             clear_history_for_chat(chat_id)
#             return await process_text_message(text, chat_id)
#         else:
#             raise e

#     ai_response = chat_completion.choices[0].message.content
#     history.append({"role": "assistant", "content": ai_response})

#     # Save current chat history
#     try:
#         s3client = await get_s3_client()
#         async with s3client as client:
#             await client.put_object(
#                 Bucket=S3_BUCKET_NAME,
#                 Key=f"{chat_id}.json",
#                 Body=json.dumps(history),
#             )
#     except Exception:
#         pass

#     return ai_response
