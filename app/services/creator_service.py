import logging
from typing import Dict, Optional

from app.events.event_executor_registry import EventExecutorRegistry
from app.services.resource_service import fetch_profile_analytics, find_profiles, fetch_content_information, \
    fetch_basic_creator_profile


async def get_basic_creator_profile(params: Optional[Dict]) -> Optional[Dict]:
    profile: Dict = await fetch_basic_creator_profile(params=params)

    if not profile:
        logging.error(f"Profile does not exists with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_fetch_event_handler(data=profile)

    return profile


async def search_profiles(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    profiles: Dict = await find_profiles(request_body=request_body, params=params)

    if not profiles:
        logging.error(f"Profiles does not exists with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_search_event_handler(data=profiles)

    return profiles


async def profile_analytics(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    profile_analytics: Dict = await fetch_profile_analytics(request_body=request_body, params=params)

    if not profile_analytics:
        logging.error(f"Profile-Analytics does not exists with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_analytics_event_handler(data=profile_analytics)

    return profile_analytics


async def fetch_contents(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    contents_information: Dict = await fetch_content_information(request_body=request_body, params=params)

    if not contents_information:
        logging.error(f"Contents information does not exists with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.content_fetch_event_handler(data=contents_information)

    return contents_information
