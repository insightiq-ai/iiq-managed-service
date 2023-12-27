from fastapi import APIRouter

from app.api_v1.endpoints.creators import api_creator_processor

api_router = APIRouter(tags=["CREATOR"])
api_router.include_router(api_creator_processor.api_router, prefix="/social/creators")
