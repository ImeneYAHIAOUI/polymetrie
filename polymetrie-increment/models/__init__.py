from .redis_models import *
from .postgres_models import *

postgres_session = create_postgres_engine_and_session(postgres_url)
redis_conn = create_redis_engine_and_session(redis_url)

def register_models(app):
    app.config["POSTGRES_SESSION"] = postgres_session
    app.config["REDIS_SESSION"] = redis_conn