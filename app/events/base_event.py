from abc import ABC
from typing import Dict


class BaseEvent(ABC):
    def __init__(self):
        # super(BaseEvent, self).__init__()
        pass

    @classmethod
    async def accounts_connected_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def accounts_disconnected_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profiles_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profiles_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profiles_audience_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profiles_audience_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def contents_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def contents_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_comments_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_comments_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_groups_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_groups_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def commerce_transactions_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def commerce_transactions_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def social_transactions_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def social_transactions_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def commerce_payouts_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def commerce_payouts_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def social_payouts_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def social_payouts_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def balances_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def balances_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def activity_artists_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def activity_artists_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def activity_contents_added_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def activity_contents_updated_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def contents_publish_success_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def contents_publish_failure_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def contents_publish_ready_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def session_expired_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def user_created_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def sdk_token_created_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_fetch_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profile_analytics_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def profile_search_event_handler(cls, data: Dict):
        pass


    @classmethod
    async def profile_fetch_event_handler(cls, data: Dict):
        pass
