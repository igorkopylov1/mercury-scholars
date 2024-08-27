import logging

from .libs.base_rest_config import BaseRestConfig

logger = logging.getLogger(__name__)


class Config(BaseRestConfig):
    _required = {"TG_BOT_TOKEN", "PROXY_API_KEY", "YANDEX_KEY_ID", "YANDEX_KEY_SECRET"}

    @classmethod
    def initialize(cls):
        cls.TG_BOT_TOKEN = cls.get("TG_BOT_TOKEN", "tg_token")
        cls.TG_BOT_CHATS = cls.get("TG_BOT_CHATS", "chats").lower().split(",")  # TODO: delete option, integrate with redis, orm
        cls.PROXY_API_KEY = cls.get("PROXY_API_KEY", "api_token")
        cls.YANDEX_KEY_ID = cls.get("YANDEX_KEY_ID", None)
        cls.YANDEX_KEY_SECRET = cls.get("YANDEX_KEY_SECRET", None)
        cls.ADMIN_CHAT_ID = int(cls.get("ADMIN_CHAT_ID", None))
        cls.HOST = cls.get("HOST", "194.87.248.10")
        cls.PORT = int(cls.get("PORT", 8443))
