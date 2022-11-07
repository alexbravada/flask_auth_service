import abc
from config.settings import Settings


SETTINGS = Settings()


class AbstractCacheStorage(abc.ABC):
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

# class RedisStorage(AbstractCacheStorage):
#     def __init__(self):
#         redis = redis.Redis(**SETTINGS.Redis.dict(), decode_responses=True)
        