import abc
from redis import Redis
from app.config.settings import PGDSN, RedisDSNDSN, Settings



redis.redis = await aioredis.create_redis_pool(
    (settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20
)

class AbstractCacheStorage(abc.ABC):
    @abstractmethod
    def get():
        pass

    @abstractmethod
    def set():
        pass


class RedisStorage(AbstractCacheStorage):
    def __init__(self):
        redis = **Settings.Redis.dict()
        