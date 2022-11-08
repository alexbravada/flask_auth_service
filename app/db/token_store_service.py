import datetime
from db.redis_base import RedisStorage
from db.redis_base import AbstractCacheStorage


class TokenStoreService(RedisStorage):
    def __init__(self):
        self.storage: AbstractCacheStorage = super().__init__()
        #print('\n\n\n\n', self.storage.redis.set('t1', 't2', ex=datetime.timedelta(seconds=66)))
    
    def add_to_blacklist(self, token, body, expired_time=1800):
        TTL = expired_time 
        self.storage.set(token, json.dumps(body), ex=datetime.timedelta(seconds=60))

    def check_blacklist(self, token):
        token = self.store.get(token)
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
