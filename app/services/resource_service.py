import json
import urllib.parse
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID

from httpx import BasicAuth
from retrying_async import retry

from app.core.config import settings
from app.schemas.enum import Environment, WebhookEvent
from app.schemas.user_schemas import UserRequest, SdkTokenRequest
from app.utils.constants import SANDBOX_BASE_URL, STAGING_BASE_URL, PRODUCTION_BASE_URL
from app.utils.exceptions import TooManyRequestException
from app.utils.network_utils import invoke_post_url, invoke_get_url, invoke_put_url


def get_base_url():
    if settings.ENVIRONMENT == Environment.SANDBOX:
        return SANDBOX_BASE_URL

    elif settings.ENVIRONMENT == Environment.STAGING:
        return STAGING_BASE_URL

    elif settings.ENVIRONMENT == Environment.PRODUCTION:
        return PRODUCTION_BASE_URL


def get_auth():
    return BasicAuth(username=str(settings.TENANT_APP_ID), password=str(settings.TENANT_APP_SECRET))


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def create_users(user_request: UserRequest) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/users")

    response: Dict = await invoke_post_url(url=url, body=user_request.json(), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def create_sdk_token(sdk_token_request: SdkTokenRequest) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/sdk-tokens")

    response: Dict = await invoke_post_url(url=url, body=sdk_token_request.json(), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_account_by_id(account_id: str) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), f"/v1/accounts/{account_id}")

    response: Dict = await invoke_get_url(url=url, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_profile_by_id(profile_id: str) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), f"/v1/profiles/{profile_id}")

    response: Dict = await invoke_get_url(url=url, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_profile_audience_by_account_id(account_id: str) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), f"/v1/audience")
    params = {
        "account_id": account_id
    }

    response: Dict = await invoke_get_url(url=url, auth=get_auth(), query=params)
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_contents_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/social/contents/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_content_comments_by_content_id_account_id(content_id: str, account_id: str, limit: int = 100,
                                                          offset: int = 0) -> Dict:
    body = {
        "content_id": content_id,
        "account_id": account_id,
        "limit": limit,
        "offset": offset
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/social/comments")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_content_groups_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/social/content-groups/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_social_transactions_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/social/income/transactions/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_commerce_transactions_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/commerce/income/transactions/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_social_payouts_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/social/income/payouts/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_commerce_payouts_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/commerce/income/payouts/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_balances_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/commerce/income/balances/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_activity_artists_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/media/activity/artists/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_activity_contents_by_ids(ids: List[str]) -> Dict:
    body = {
        "ids": ids
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/media/activity/contents/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(body), headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_publish_content_by_id(id: str) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), f"/v1/social/contents/publish/{id}")

    response: Dict = await invoke_get_url(url=url, headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response

@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_basic_creator_profile(params: Optional[Dict]) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/social/creators/profiles")

    response: Dict = await invoke_get_url(url=url, headers={}, auth=get_auth(), query=params)
    # TODO do error-handling over here

    return response

@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def find_profiles(request_body: object, params: Optional[Dict]) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/social/creators/profiles/search")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(request_body), query=params,
                                           headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_profile_analytics(request_body: object, params: Optional[Dict]) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/social/creators/profiles/analytics")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(request_body), query=params,
                                           headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_content_information(request_body: object, params: Optional[Dict]) -> Dict:

    url = urllib.parse.urljoin(get_base_url(), "/v1/social/creators/contents/fetch")

    response: Dict = await invoke_post_url(url=url, body=json.dumps(request_body), query=params,
                                           headers={}, auth=get_auth())
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def fetch_all_webhooks() -> Dict:
    params = {
        "limit": 100,
        "offset": 0
    }
    url = urllib.parse.urljoin(get_base_url(), "/v1/webhooks")

    response: Dict = await invoke_get_url(url=url, headers={}, auth=get_auth(), query=params)
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def create_webhook(webhook_url: str, events: List[WebhookEvent]) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), "/v1/webhooks")

    body = {
        "name": f"MANAGED_SERVICE_WEBHOOK_{int(datetime.now().timestamp())}",
        "url": webhook_url,
        "events": events,
        "is_active": True
    }

    response: Dict = await invoke_post_url(url=url, headers={}, auth=get_auth(), body=json.dumps(body))
    # TODO do error-handling over here

    return response


@retry(attempts=3, delay=1, retry_exceptions=(TooManyRequestException,))
async def update_webhook(id: UUID, name: str, webhook_url: str, events: List[WebhookEvent]) -> Dict:
    url = urllib.parse.urljoin(get_base_url(), f"/v1/webhooks/{id}")

    body = {
        "name": name,
        "url": webhook_url,
        "events": events,
        "is_active": True
    }

    response: Dict = await invoke_put_url(url=url, headers={}, auth=get_auth(), body=json.dumps(body))
    # TODO do error-handling over here

    return response
