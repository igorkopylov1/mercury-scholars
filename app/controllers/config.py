import logging
import typing as tp

from ..tg import BaseTgClient


logger = logging.getLogger(__name__)


class OperationsController:
    def __init__(
        self,
        tg_base_client: BaseTgClient,
    ):
        self.tg_base_client = tg_base_client

    @staticmethod
    def _escape_json_str(json_str: str) -> str:
        return json_str.replace("{", "{{").replace("}", "}}")

    async def create_response(self, chat_id: int, message_text: str) -> str: # TODO: add enum
        await self.tg_base_client.send_chat_action(chat_id=chat_id, action='typing')
        # TODO: add autorithation
        try:
            await self.tg_base_client.process_comand(chat_id, message_text)
        except Exception as e:
            raise e  # TODO: processing except
        
        return "ok"

