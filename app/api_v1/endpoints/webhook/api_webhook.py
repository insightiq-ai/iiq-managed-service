from fastapi import APIRouter

from app.api_v1.endpoints.webhook import api_webhook_processor

api_router = APIRouter(tags=["WEBHOOK"])
api_router.include_router(api_webhook_processor.api_router, prefix="/webhook")
