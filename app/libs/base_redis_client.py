import aioredis
import subprocess

import time
import logging
import typing as tp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseRedisClient:
    def __init__(self, host=None, port=None, password=None, socket_timeout=1, *, db=None) -> None:
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout
        self.redis = None
    
    def _run_server(self):
        config_file = '/etc/redis/redis.conf'
        try:
            subprocess.run(['sudo', 'redis-server', config_file], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error while starting Redis: {e}")
    
    def check_connection(self) -> bool:
        return bool(self.redis)
    
    async def connect(self) -> None:
        try:
            self.redis = await aioredis.from_url(
                f"redis://{self.host}:{self.port}/{self.db}",
                password=self.password,
                socket_timeout=self.socket_timeout
            )
        except aioredis.exceptions.ConnectionError:
            self._run_server()
            self.redis = await aioredis.from_url(
                f"redis://{self.host}:{self.port}/{self.db}",
                password=self.password,
                socket_timeout=self.socket_timeout
            )
    
    async def get_value(self, *args, **kwargs) -> None:
        raise NotImplementedError("Define get method")
    
    async def set_value(self, *args, **kwargs) -> None:
        raise NotImplementedError("Define set method")
    
    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None
