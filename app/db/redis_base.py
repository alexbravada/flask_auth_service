from abc import ABC
from abc import abstractmethod
from config.settings import Settings
import redis


SETTINGS = Settings()


class AbstractCacheStorage(ABC):
    @abstractmethod
    def get():
        pass

    @abstractmethod
    def set():
        pass


# class AbstractCacheStorage(ABC):
#     @abstractmethod
#     def get(self, key: str, **kwargs):
#         pass

#     @abstractmethod
#     def set(self, key: str, value: str, expire: int, **kwargs):
#         pass

class RedisStorage(AbstractCacheStorage):
    def __init__(self):
        self.redis = redis.Redis(**SETTINGS.Redis.dict(), decode_responses=True)

def get_redis():
    return redis.Redis(**SETTINGS.Redis.dict(), decode_responses=True)
