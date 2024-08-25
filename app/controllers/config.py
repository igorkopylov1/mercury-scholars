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

    def first_try(self)->None:
        print("Success")
