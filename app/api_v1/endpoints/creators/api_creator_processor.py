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


@api_router.get("/dictionary/interests", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_interests(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_interests(params=dict(request.query_params.items()))


@api_router.get("/dictionary/topics", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_topics(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_topics(params=dict(request.query_params.items()))


@api_router.get("/dictionary/userhandles", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_userhandles(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_userhandles(params=dict(request.query_params.items()))


@api_router.post("/profiles/quick-search", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def quick_search_profiles(request: Request,
                                request_body: Optional[object] = Body(default=None)) -> Optional[Dict]:
    return await creator_service.quick_search_profiles(request_body=request_body, params=dict(request.query_params.items()))


@api_router.get("/dictionary/languages", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_languages(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_languages(params=dict(request.query_params.items()))


@api_router.get("/dictionary/brands", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_brands(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_brands(params=dict(request.query_params.items()))


@api_router.get("/dictionary/locations", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_locations(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_locations(params=dict(request.query_params.items()))


@api_router.get("/dictionary/topics/relevance", status_code=HTTPStatus.OK, response_model=Optional[Dict])
async def get_dictionary_relevant_topics(request: Request) -> Optional[Dict]:
    return await creator_service.get_dictionary_relevant_topics(params=dict(request.query_params.items()))
