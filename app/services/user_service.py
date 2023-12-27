import logging
from typing import Dict, Optional

from app.events.event_executor_registry import EventExecutorRegistry
from app.schemas.user_schemas import UserRequest, SdkTokenRequest
from app.services.resource_service import create_users, create_sdk_token


async def create_user(user_request: UserRequest) -> Optional[Dict]:
    user: Dict = await create_users(user_request=user_request)

    if not user:
        logging.error(f"Unable to create user with requested body")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.user_created_event_handler(data=user)

    return user


async def generate_sdk_token(sdk_token_request: SdkTokenRequest) -> Optional[Dict]:
    sdk_token: Dict = await create_sdk_token(sdk_token_request=sdk_token_request)

    if not sdk_token:
        logging.error(f"Unable to create sdk-token with requested body")

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.sdk_token_created_event_handler(data=sdk_token)

    return sdk_token
