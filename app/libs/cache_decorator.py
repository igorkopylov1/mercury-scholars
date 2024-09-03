import time
import logging
from collections import OrderedDict
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTLCache:
    def __init__(self, maxsize=100, ttl=60):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_time = time.time()
            key = (args, frozenset(kwargs.items()))

            if key in self.cache:
                value, timestamp = self.cache[key]
                if current_time - timestamp < self.ttl:
                    return value
                else:
                    del self.cache[key]

            result = await func(*args, **kwargs)
            self.cache[key] = (result, current_time)
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)

            return result

        return wrapper


def ttl_cache(maxsize=100, ttl=60):
    return TTLCache(maxsize=maxsize, ttl=ttl)
