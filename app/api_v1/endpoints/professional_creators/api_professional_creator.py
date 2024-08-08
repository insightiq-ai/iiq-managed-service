from fastapi import APIRouter

from app.api_v1.endpoints.professional_creators import api_professional_creator_processor

api_router = APIRouter(tags=["CREATOR"])
api_router.include_router(api_professional_creator_processor.api_router, prefix="/professional/creators")
