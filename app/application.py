import logging
import typing as tp

from .config import Config
from . import api  # noqa
from .controllers import OperationsController
# from .db import clients, dao  # TODO: ADD
from .libs import BaseApplication
from .tg import BaseTgClient, S3Manager


logger = logging.getLogger(__name__)

# integrate with different clients such as: history client, math ...(dao)
class Application(BaseApplication):
    def __init__(
        self,
        tg_base_client: tp.Optional[BaseTgClient] = None,
    ) -> None:
        super().__init__()
        tg_client = tg_base_client or BaseTgClient(tg_bot_token=Config.TG_BOT_TOKEN,
            proxi_api_key=Config.PROXY_API_KEY,
        )
        s3client = S3Manager()
        self.operation_controller = OperationsController(tg_base_client=tg_client, s3client=s3client)
        # self._pg_client = clients.PGClient(pg_url or Config.ASYNC_PG_URL)  # TODO: Add client
