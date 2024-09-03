import logging

from .libs.base_rest_config import BaseRestConfig

logger = logging.getLogger(__name__)


class Config(BaseRestConfig):
    _required = {"TG_BOT_TOKEN", "PROXY_API_KEY", "YANDEX_KEY_ID", "YANDEX_KEY_SECRET", "ADMIN_CHAT_ID", "REDIS_PASSWORD", "DB_PASSWORD", "DB_DATABASE"}

    @classmethod
    def initialize(cls):
        cls.TG_BOT_TOKEN = cls.get("TG_BOT_TOKEN", "tg_token")
        cls.TG_BOT_CHATS = cls.get("TG_BOT_CHATS", "chats").lower().split(",")  # TODO: delete option, integrate with redis, orm

        cls.PROXY_API_KEY = cls.get("PROXY_API_KEY", "api_token")
        
        # Yandex s3 settings
        cls.YANDEX_KEY_ID = cls.get("YANDEX_KEY_ID", None)
        cls.YANDEX_KEY_SECRET = cls.get("YANDEX_KEY_SECRET", None)
        cls.ADMIN_CHAT_ID = int(cls.get("ADMIN_CHAT_ID", None))
        cls.HOST = cls.get("HOST", "194.87.248.10")
        
        # Redis settings
        cls.REDIS_HOST = cls.get("REDIS_HOST", "localhost")
        cls.REDIS_PORT = cls.get("REDIS_PORT", "6379")
        cls.REDIS_PASSWORD = cls.get("REDIS_PASSWORD", "huckme")
        cls.PORT = int(cls.get("PORT", 8443))
        cls.TIMEZONE = "Europe/Moscow"

        # PG settings
        DB_USERNAME=cls.get("DB_USERNAME", "Gosha Kucenko")
        DB_PASSWORD=cls.get("DB_PASSWORD", "huckme")
        DB_HOSTNAME=cls.get("DB_HOSTNAME", "localhost")
        DB_PORT=cls.get("DB_PORT", "port")
        DB_DATABASE=cls.get("DB_DATABASE", "db_dev")
        cls.DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
