import logging
import typing as tp

from .config import Config
from . import api  # noqa
from .controllers import OperationsController
from .libs import BaseApplication
from .tg import BaseTgClient, S3Manager, SessionRedisClient, AuthorizeRedisClient
from .db import PGClient


logger = logging.getLogger(__name__)

# integrate with different clients such as: history client, math ...(dao)
class Application(BaseApplication):
    def __init__(
        self,
        tg_client: tp.Optional[BaseTgClient] = None,
        s3client: tp.Optional[S3Manager] = None,
        session_redis_client: tp.Optional[SessionRedisClient] = None,
        authorize_redis_client: tp.Optional[AuthorizeRedisClient] = None,
        pg_url: tp.Optional[str] = None,
    ) -> None:
        super().__init__()
        self.tg_client = tg_client or BaseTgClient(tg_bot_token=Config.TG_BOT_TOKEN,
            proxi_api_key=Config.PROXY_API_KEY,
        )
        self.s3client = s3client or S3Manager()
        self.session_redis_client = session_redis_client or SessionRedisClient()
        self.authorize_redis_client = authorize_redis_client or AuthorizeRedisClient()
        self.pg_client = PGClient(pg_url or Config.DATABASE_URL)
        self.operation_controller = OperationsController(
            tg_base_client=self.tg_client,
            s3client=self.s3client,
            session_redis_client=self.session_redis_client,
            authorize_redis_client=self.authorize_redis_client,
            pg_client=self.pg_client,
        )
