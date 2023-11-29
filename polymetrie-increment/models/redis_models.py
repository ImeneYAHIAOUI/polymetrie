from config.db import redis_url

import redis

class Increment:
    def __init__(self, url, incvalue):
        self.url = url
        self.incvalue = incvalue

def create_redis_engine_and_session(redis_url):
    return redis.StrictRedis.from_url(redis_url)
