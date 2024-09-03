import json
import logging
import typing as tp

import asyncio
from datetime import datetime

from ...libs import BaseRedisClient
from ... import schema as schema
from ...config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthorizeRedisClient(BaseRedisClient):
    def __init__(self, host=None, port=None, db=2, password=None, socket_timeout=None) -> None:
        host = host or Config.REDIS_HOST
        port = port or Config.REDIS_PORT
        password = password or Config.REDIS_PASSWORD
        super().__init__(host=host, port=port, password=password, socket_timeout=socket_timeout)
        super().__init__(host=host, port=port, password=password, socket_timeout=socket_timeout)
        self.db = db
        self.redis = None

    async def set_value(self, data: schema.redis.RedisAuthorize) -> None:
        json_value = json.dumps(data.dict())

        await self.redis.set(data.chat_id, json_value)

    async def get_value(self, key: str) -> tp.Optional[schema.redis.RedisAuthorize]:
        json_value = await self.redis.get(key)
        if json_value is not None:
            data = json.loads(json_value)
            return schema.redis.RedisAuthorize(**data) 
        return None
    

class SessionRedisClient(BaseRedisClient):
    def __init__(self, host=None, port=None, db=1, password=None, socket_timeout=None) -> None:
        host = host or Config.REDIS_HOST
        port = port or Config.REDIS_PORT
        password = password or Config.REDIS_PASSWORD
        super().__init__(host=host, port=port, password=password, socket_timeout=socket_timeout)
        self.db = db
        self.redis = None

    async def set_value(self, data: schema.redis.RedisSession) -> None:
        json_value = json.dumps(data.to_dict())

        await self.redis.set(data.chat_id, json_value)

    async def get_value(self, key: str) -> tp.Optional[schema.redis.RedisSession]:
        json_value = await self.redis.get(key)
        if json_value is not None:
            data = json.loads(json_value)
            logger.info(f"get_value from redis storage data: {data}")
            return schema.redis.RedisSession(**data) 
        return None
