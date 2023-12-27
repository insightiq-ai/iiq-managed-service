from uuid import UUID

from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings, URLPath

from app.schemas.enum import Environment

config = Config(".env")


class Settings:
    APP_NAME = config("APP_NAME", cast=str, default='IIQ_MANAGED_SERVICE')
    ENVIRONMENT = config("ENVIRONMENT", cast=Environment, default="SANDBOX")
    TENANT_APP_ID = config("TENANT_APP_ID", cast=UUID, default='19566e1b-e4d4-42ee-84a9-5550afca7cd0')
    TENANT_APP_SECRET = config("TENANT_APP_SECRET", cast=Secret, default='27eb3d5b-66b7-4204-9148-6d9395873f3a')
    LOG_LEVEL = config("LOG_LEVEL", cast=str, default="DEBUG")

    SUPPORTED_PRODUCTS = config("SUPPORTED_PRODUCTS", cast=CommaSeparatedStrings)
    EVENT_EXECUTORS = config("EVENT_EXECUTORS", cast=CommaSeparatedStrings, default=None)
    WEBHOOK_BASE_URL = config("WEBHOOK_BASE_URL", cast=URLPath)


settings = Settings()
