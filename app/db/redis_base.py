import abc
import redis
from app.config.settings import Settings


SETTINGS = Settings()


class AbstractCacheStorage(abc.ABC):
    @abstractmethod
    def get():
        pass

    @abstractmethod
    def set():
        pass


class RedisStorage(AbstractCacheStorage):
    def __init__(self):
        redis = redis.Redis(**SETTINGS.Redis.dict(), decode_responses=True)
        