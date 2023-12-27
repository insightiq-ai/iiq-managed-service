import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api_v1.endpoints.connect import api_user
from app.api_v1.endpoints.creators import api_creator
from app.api_v1.endpoints.webhook import api_webhook
from app.core.config import settings
from app.utils.setup_config import configure_webhooks, register_event_listeners
from app.utils.validator import validate_products

app = FastAPI()

app.include_router(api_webhook.api_router, prefix='/v1')
app.include_router(api_creator.api_router, prefix='/v1')
app.include_router(api_user.api_router, prefix='/v1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "I'm up"}


@app.on_event("startup")
async def start_service():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    validate_products(settings.SUPPORTED_PRODUCTS)
    await register_event_listeners(settings.EVENT_EXECUTORS)
    await configure_webhooks()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000, proxy_headers=True, forwarded_allow_ips="*", use_colors=True,
                env_file="../.env")
