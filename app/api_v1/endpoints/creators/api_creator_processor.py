from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Body
from starlette.requests import Request

from app.services import creator_service

api_router = APIRouter()

@api_router.get("/profiles", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_basic_creator_profile(request: Request) -> Optional[Dict]:
    return await creator_service.get_basic_creator_profile(params=dict(request.query_params.items()))

@api_router.post("/profiles/search", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def search_profiles(request: Request,
                          request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.search_profiles(request_body=request_body, params=dict(request.query_params.items()))


@api_router.post("/profiles/analytics", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def profile_analytics(request: Request,
                            request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.profile_analytics(request_body=request_body, params=dict(request.query_params.items()))


@api_router.post("/contents/fetch", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def fetch_contents(request: Request,
                         request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.fetch_contents(request_body=request_body, params=dict(request.query_params.items()))
