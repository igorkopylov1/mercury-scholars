import logging
import typing as tp

from .config import Config
from . import api  # noqa
from .controllers import OperationsController
# from .db import clients, dao  # TODO: ADD
from .libs import BaseApplication
from .tg import BaseTgClient


logger = logging.getLogger(__name__)

# integrate with different clients such as: history client, math ...(dao)
class Application(BaseApplication):
    def __init__(
        self,
        tg_base_client: tp.Optional[BaseTgClient] = None,
    ) -> None:
        super().__init__()
        tg_client = tg_base_client or BaseTgClient()
        self.operation_controller = OperationsController(tg_base_client=tg_client)
        self.app.state.application = self
        # self._pg_client = clients.PGClient(pg_url or Config.ASYNC_PG_URL)  # TODO: Add client
