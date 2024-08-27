import logging
import typing as tp
import aioboto3

from ..tg import BaseTgClient, S3Manager
from ..config import Config


logger = logging.getLogger(__name__)


class OperationsController:
    BUCKET_NAME = "igorkopylov"

    def __init__(
        self,
        tg_base_client: BaseTgClient,
        s3client: S3Manager,
    ):
        self.tg_base_client = tg_base_client
        self.s3client = s3client

    @staticmethod
    def _escape_json_str(json_str: str) -> str:
        return json_str.replace("{", "{{").replace("}", "}}")

    async def create_response(self, chat_id: int, message_text: str, user_name: str) -> str: # TODO: add enum
        await self.tg_base_client.send_chat_action(chat_id=chat_id, action='typing')
        # TODO: add autorithation, add buckets
        session = aioboto3.Session(
            aws_access_key_id=Config.YANDEX_KEY_ID,
            aws_secret_access_key=Config.YANDEX_KEY_SECRET
        )
        history_content = await self.s3client.read_file(session=session, bucket_name=self.BUCKET_NAME, key=str(chat_id))
        history = f"{history_content}\n {message_text}"  # TODO: add prompt text
        
        try:
            await self.tg_base_client.process_comand(chat_id, history, user_name)
        except Exception as e:
            raise e  # TODO: processing except
        await self.s3client.write_file(session=session, bucket_name=self.BUCKET_NAME, key=str(chat_id), content=message_text) # TODO: ? history)

        return "ok"

