import logging
from typing import Dict, Optional

from app.events.event_executor_registry import EventExecutorRegistry
from app.services.resource_service import fetch_profile_analytics, fetch_search_profiles, fetch_content_information, \
    fetch_basic_creator_profile, fetch_dictionary_interests, fetch_dictionary_topics, fetch_dictionary_userhandles, \
    fetch_quick_search_profiles, fetch_dictionary_languages, fetch_dictionary_brands, fetch_dictionary_locations, \
    fetch_professional_profile_analytics


async def get_basic_creator_profile(params: Optional[Dict]) -> Optional[Dict]:
    profile: Dict = await fetch_basic_creator_profile(params=params)

    if not profile:
        logging.error(f"Profile does not exists with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_fetch_event_handler(data=profile)

    return profile


async def search_profiles(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    profiles: Dict = await fetch_search_profiles(request_body=request_body, params=params)

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


async def get_dictionary_interests(params: Optional[Dict]) -> Optional[Dict]:
    interests: Dict = await fetch_dictionary_interests(params=params)

    if not interests:
        logging.error(f"Interests do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_interests_event_handler(data=interests)

    return interests


async def get_dictionary_topics(params: Optional[Dict]) -> Optional[Dict]:
    topics: Dict = await fetch_dictionary_topics(params=params)

    if not topics:
        logging.error(f"Topics do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_topics_event_handler(data=topics)

    return topics


async def get_dictionary_userhandles(params: Optional[Dict]) -> Optional[Dict]:
    userhandles: Dict = await fetch_dictionary_userhandles(params=params)

    if not userhandles:
        logging.error(f"Userhandles do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_userhandles_event_handler(data=userhandles)

    return userhandles


async def quick_search_profiles(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    profiles: Dict = await fetch_quick_search_profiles(request_body=request_body, params=params)

    if not profiles:
        logging.error(f"Profiles do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_quick_search_event_handler(data=profiles)

    return profiles


async def get_dictionary_languages(params: Optional[Dict]) -> Optional[Dict]:
    languages: Dict = await fetch_dictionary_languages(params=params)

    if not languages:
        logging.error(f"Languages do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_languages_event_handler(data=languages)

    return languages


async def get_dictionary_brands(params: Optional[Dict]) -> Optional[Dict]:
    brands: Dict = await fetch_dictionary_brands(params=params)

    if not brands:
        logging.error(f"Brands do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_brands_event_handler(data=brands)

    return brands


async def get_dictionary_locations(params: Optional[Dict]) -> Optional[Dict]:
    locations: Dict = await fetch_dictionary_locations(params=params)

    if not locations:
        logging.error(f"Locations do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_locations_event_handler(data=locations)

    return locations


async def professional_profile_analytics(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    professional_profile_analytics: Dict = await fetch_professional_profile_analytics(request_body=request_body, params=params)

    if not professional_profile_analytics:
        logging.error(f"Profile Analytics do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_analytics_event_handler(data=professional_profile_analytics)

    return professional_profile_analytics
