from redis_base import RedisStorage
from db.redis_base import AbstractCacheStorage


class TokenStoreService:
    def __init__(self):
        self.store: AbstractCacheStorage = RedisStorage()
    
    def add_to_blacklist(self, token, expired_time):
        TTL = expired_time 
        self.storage.set(token, TTL)
        
    def check_blacklist(self, token):
        token = self.store.get(token)

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
        