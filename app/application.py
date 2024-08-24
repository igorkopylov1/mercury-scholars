import logging
import typing as tp

from .config import Config
from . import api  # noqa
# from .controllers import OperationsController  # TODO: ADD
# from .db import clients, dao
from .libs import BaseApplication
from .tg import BaseTgClient


logger = logging.getLogger(__name__)


# class for integrate with different clients sach as: history client, math ...(dao)


class Application(BaseApplication):
    def __init__(
        self,
        tg_client: tp.Optional[BaseTgClient] = None,
        # pg_url: str | None = None,
        # *args: tp.Any,
        # **kwargs: tp.Any,
    ) -> None:
        super().__init__()
        self.tg_client = tg_client or BaseTgClient()
        pass
        # self._pg_client = clients.PGClient(pg_url or Config.ASYNC_PG_URL)  # TODO: Add client
