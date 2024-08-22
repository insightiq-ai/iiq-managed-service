from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Body
from starlette.requests import Request

from app.services import creator_service

api_router = APIRouter()


@api_router.post("/profiles/analytics", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def profile_analytics(request: Request, request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.professional_profile_analytics(request_body=request_body, params=dict(request.query_params.items()))


@api_router.post("/contents/fetch", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def fetch_professional_contents(request: Request,
                                      request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.post_professional_contents_fetch(request_body=request_body, params=dict(request.query_params.items()))
