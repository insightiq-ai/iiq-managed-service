from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.events.db.db_config import db_settings


def get_sqlalchemy_pg_database_uri() -> str:
    sqlalchemy_pg_scheme = "postgresql+asyncpg"

    return PostgresDsn.build(
        scheme=sqlalchemy_pg_scheme,
        user=db_settings.DB_USER,
        password=str(db_settings.DB_PASSWORD),
        host=db_settings.DB_HOST,
        port=db_settings.DB_PORT,
        path=f"/{db_settings.DB_NAME or ''}",
    )


async_engine = create_async_engine(get_sqlalchemy_pg_database_uri(),
                                   pool_pre_ping=db_settings.DB_POOL_PRE_PING,
                                   pool_size=db_settings.DB_POOL_SIZE,
                                   echo=db_settings.DB_ECHO_POOL,
                                   max_overflow=db_settings.DB_MAX_OVERFLOW,
                                   pool_recycle=db_settings.DB_POOL_RECYCLE_IN_SECONDS,
                                   echo_pool=db_settings.DB_ECHO_POOL,
                                   pool_reset_on_return=db_settings.DB_POOL_RESET_ON_RETURN,
                                   pool_timeout=db_settings.DB_POOL_TIMEOUT_IN_SECONDS,
                                   connect_args={"server_settings": {"jit": "off"}})

AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=True, expire_on_commit=False)
