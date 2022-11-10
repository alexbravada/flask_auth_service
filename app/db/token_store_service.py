import datetime
from db.redis_base import RedisStorage
from db.redis_base import AbstractCacheStorage
from db.redis_base import get_redis
import json
from functools import lru_cache
import redis


#class TokenStoreService(RedisStorage):
class TokenStoreService:
    def __init__(self, repository: AbstractCacheStorage):
        #self.storage: AbstractCacheStorage = super().__init__()
        #self.storage = RedisStorage(conn = get_redis())
        self.storage = repository
    def add_to_blacklist(self, token, body, ttl=600):
        self.storage.set(token, json.dumps(body), ex=datetime.timedelta(seconds=ttl))

    def check_blacklist(self, token):
        token = self.storage.get(token)
        return token

    def add_user_refresh(self, user, refresh):
        pass
    
    def set_user_payload(self):
        '''username: {
            "refresh": [refreshes] # max_len == 10,
            "payload": {"name": Alex}
        }
'''
        pass
    
    def get_user_payload(self):
        pass


@lru_cache()
def get_token_store_service(
    storage: redis.Redis = get_redis()
) -> TokenStoreService:
    return TokenStoreService(storage) 
