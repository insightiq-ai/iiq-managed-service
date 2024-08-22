import logging
from fastapi import HTTPException
from typing import Dict, Optional

from app.core.config import settings
from app.events.event_executor_registry import EventExecutorRegistry
from app.schemas.enum import Product
from app.services.resource_service import fetch_profile_analytics, fetch_search_profiles, fetch_content_information, \
    fetch_basic_creator_profile, fetch_dictionary_interests, fetch_dictionary_topics, fetch_dictionary_userhandles, \
    fetch_quick_search_profiles, fetch_dictionary_languages, fetch_dictionary_brands, fetch_dictionary_locations, \
    fetch_dictionary_relevant_topics, fetch_contact_info, fetch_professional_profile_analytics, \
    post_async_profile_analytics_request, post_async_contents_fetch_request, post_audience_overlap_request


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


async def get_dictionary_relevant_topics(params: Optional[Dict]) -> Optional[Dict]:
    relevant_topics: Dict = await fetch_dictionary_relevant_topics(params=params)

    if not relevant_topics:
        logging.error(f"Relevant topics do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.dictionary_relevant_topics_event_handler(data=relevant_topics)

    return relevant_topics


async def get_contact_info(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    profiles: Dict = await fetch_contact_info(request_body=request_body, params=params)

    if not profiles:
        logging.error(f"Contact info for the profiles do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.profile_contact_info_event_handler(data=profiles)

    return profiles


async def professional_profile_analytics(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    analytics: Dict = await fetch_professional_profile_analytics(request_body=request_body, params=params)

    if not analytics:
        logging.error(f"Profile Analytics do not exist with requested-filters")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.professional_profile_analytics_event_handler(data=analytics)

    return analytics


async def post_async_profile_analytics(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    # Check if the product is supported
    if Product.CREATOR_SEARCH not in settings.SUPPORTED_PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"{Product.CREATOR_SEARCH} is not supported. \
            Please add it to SUPPORTED_PRODUCTS in config to enable this API."
        )

    response_data: Dict = await post_async_profile_analytics_request(request_body=request_body,params=params)

    if not response_data:
        logging.error(f"Profile Analytics do not exist with requested filters: {request_body}")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.async_profile_analytics_request_event_handler(data=response_data)

    return response_data


async def post_async_contents_fetch(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    # Check if the product is supported
    if Product.PUBLIC_CONTENT_SEARCH not in settings.SUPPORTED_PRODUCTS:
        raise HTTPException(status_code=400, detail=f"{Product.PUBLIC_CONTENT_SEARCH} is not supported.")

    response_data: Dict = await post_async_contents_fetch_request(request_body=request_body, params=params)

    if not response_data:
        logging.error(f"Contents do not exist with requested filters: {request_body}")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.async_contents_fetch_request_event_handler(data=response_data)

    return response_data


async def post_audience_overlap(request_body: object, params: Optional[Dict]) -> Optional[Dict]:
    # Check if the product is supported
    if Product.CREATOR_SEARCH not in settings.SUPPORTED_PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"{Product.CREATOR_SEARCH} is not supported. \
            Please add it to SUPPORTED_PRODUCTS in config to enable this API."
        )

    response_data: dict = await post_audience_overlap_request(request_body=request_body, params=params)

    if not response_data:
        logging.error(f"Audience-Overlap does not exist with requested filters: {request_body}")
        return None

    for executor_event in EventExecutorRegistry.get_all_events():
        await executor_event.audience_overlap_request_event_handler(data=response_data)

    return response_data
