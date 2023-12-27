from fastapi import APIRouter

from app.api_v1.endpoints.connect import api_user_processor

api_router = APIRouter(tags=["CONNECT"])
api_router.include_router(api_user_processor.api_router, prefix="/users")
