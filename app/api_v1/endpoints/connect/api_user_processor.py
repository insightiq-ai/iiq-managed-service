from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter

from app.schemas.user_schemas import UserRequest, SdkTokenRequest
from app.services import user_service

api_router = APIRouter()


@api_router.post("", status_code=HTTPStatus.CREATED, response_model=Optional[Dict])
async def create_user(user_request: UserRequest) -> Optional[Dict]:
    return await user_service.create_user(user_request=user_request)


@api_router.post("/sdk-tokens", status_code=HTTPStatus.CREATED, response_model=Optional[Dict])
async def generate_sdk_token(sdk_token_request: SdkTokenRequest) -> Optional[Dict]:
    return await user_service.generate_sdk_token(sdk_token_request=sdk_token_request)
