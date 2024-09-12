import logging
import typing as tp
from datetime import datetime

from ..db import PGClient
from ..config import Config
from .. import schema as schema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBController:
    def __init__(self, pg_client: PGClient) -> None:
        self.pg_client = pg_client
    
    async def insert_chat_info(
            self,
            chat_id: str,
            first_name: str,
            start_date: str,
            end_date: str,
            pay: int
        ) -> tp.Tuple[str]:
        chat_info = dict(
            chat_id=chat_id,
            first_name=first_name,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            pay=pay
        )
        try:
            result = await self.pg_client(chat_info)
        except Exception as e:
            logger.error(f"Insert error: {e}")
            return e
        return result
