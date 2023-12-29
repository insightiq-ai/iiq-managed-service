from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class DbSettings:
    DB_ENABLED = config("DB_ENABLED", cast=bool, default=False)

    # TODO: Add mysql support
    DB_TYPE = config("DB_TYPE", cast=str, default="postgres")
    DB_USER = config("DB_USER", cast=str, default=None)
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
    DB_HOST = config("DB_HOST", cast=str, default=None)
    DB_PORT = config("DB_PORT", cast=str, default="5432")
    DB_NAME = config("DB_NAME", cast=str, default=None)
    DB_POOL_SIZE = config("DB_POOL_SIZE", cast=int, default=5)
    DB_MAX_OVERFLOW = config("DB_MAX_OVERFLOW", cast=int, default=-1)
    DB_POOL_PRE_PING = config("DB_POOL_PRE_PING", cast=bool, default=True)
    DB_ECHO = config("DB_ECHO", cast=bool, default=False)
    DB_POOL_RECYCLE_IN_SECONDS = config("DB_POOL_RECYCLE_IN_SECONDS", cast=int, default=3600)
    DB_ECHO_POOL = config("DB_ECHO_POOL", cast=bool, default=False)
    DB_POOL_RESET_ON_RETURN = config("DB_POOL_RESET_ON_RETURN", cast=str, default="rollback")
    DB_POOL_TIMEOUT_IN_SECONDS = config("DB_POOL_TIMEOUT_IN_SECONDS", cast=int, default=30)
    DB_POOL = config("DB_POOL", cast=str, default="~sqlalchemy.pool.QueuePool")

    if DB_ENABLED:
        if not DB_USER:
            raise Exception("Config missing for DB_USER")
        if not DB_PASSWORD:
            raise Exception("Config missing for DB_PASSWORD")
        if not DB_HOST:
            raise Exception("Config missing for DB_HOST")
        if not DB_NAME:
            raise Exception("Config missing for DB_NAME")


db_settings = DbSettings()
