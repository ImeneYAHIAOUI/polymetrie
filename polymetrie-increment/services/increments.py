from service import app
from .clients import query_client_by_url
from models.redis_models import Increment

redis_conn = app.config["REDIS_SESSION"]

def add_increment(url):
    client = query_client_by_url(url)
    existing_increment = redis_conn.hget('increments', url)
    if(existing_increment):
        incvalue = int(existing_increment) + 1
    else :
        incvalue = 1
    redis_conn.hset('increments', url, incvalue)

def query_all_increments():
    increments = []
    for url, incvalue in redis_conn.hgetall('increments').items():
        # increments.append(Increment(url=url.decode('utf-8'), incvalue=int(incvalue)))
        increments.append({"url": url.decode('utf-8'), "incvalue": int(incvalue)})
    return increments