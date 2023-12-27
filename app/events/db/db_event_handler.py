import logging
from typing import List, Dict, Union, Optional

from app.events.base_event import BaseEvent
from app.events.db.deps import AsyncDataStore
from app.events.db.repository.base_templated import base_templated_repository
from app.events.db.session import AsyncSessionLocal
from app.utils.mapping_utils import flatten_dict, preprocess_and_map_obj_to_another_obj, \
    preprocess_and_map_obj_list_to_another_list


class DbEventHandler(BaseEvent):

    def __init__(self):
        super(DbEventHandler, self).__init__()

    @classmethod
    async def persist_to_db(self, table_mappings: Dict, data: Union[Dict, List]):

        fields = table_mappings.get('fields')
        if not fields:
            logging.error(f"Table mapping configurations are missing. Please configure them.")
            return

        value_processors: Optional[Dict] = table_mappings.get('value_preprocessors')
        flattened_value_preprocessors: Optional[Dict] = None
        if value_processors:
            flattened_value_preprocessors = flatten_dict(value_processors)

        ds: Union[AsyncDataStore, None] = None

        try:
            ds = AsyncDataStore(db=AsyncSessionLocal())
            if isinstance(data, Dict):
                mapped_account: Dict = preprocess_and_map_obj_to_another_obj(
                    obj=data, mapping_config=flatten_dict(fields),
                    preprocess_mapping_config=flattened_value_preprocessors)
                await base_templated_repository.upsert_one(ds=ds, table=table_mappings.get('name'),
                                                           schema=table_mappings.get('schema'),
                                                           unique_key=table_mappings.get('unique_key'),
                                                           data=mapped_account)
            else:
                mapped_account: List[Dict] = preprocess_and_map_obj_list_to_another_list(
                    obj_list=data, mapping_config=flatten_dict(fields),
                    preprocess_mapping_config=flattened_value_preprocessors)

                await base_templated_repository.upsert_batch(ds=ds, table=table_mappings.get('name'),
                                                             schema=table_mappings.get('schema'),
                                                             unique_key=table_mappings.get('unique_key'),
                                                             data=mapped_account)
            await base_templated_repository.db_commit(ds=ds)
        finally:
            if ds and ds.db:
                await ds.db.close()

    @classmethod
    async def accounts_connected_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACCOUNT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACCOUNT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def accounts_disconnected_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACCOUNT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACCOUNT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def profiles_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_TABLE_MAPPINGS, data=data)

    @classmethod
    async def profiles_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_TABLE_MAPPINGS, data=data)

    @classmethod
    async def profiles_audience_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_AUDIENCE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_AUDIENCE_TABLE_MAPPINGS, data=data)

    @classmethod
    async def profiles_audience_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_AUDIENCE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_AUDIENCE_TABLE_MAPPINGS, data=data)

    @classmethod
    async def contents_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def contents_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def content_comments_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_COMMENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_COMMENT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def content_comments_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_COMMENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_COMMENT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def content_groups_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_GROUP_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_GROUP_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def content_groups_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENT_GROUP_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENT_GROUP_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def commerce_transactions_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_TRANSACTION_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_TRANSACTION_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def commerce_transactions_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_TRANSACTION_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_TRANSACTION_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def social_transactions_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import SOCIAL_TRANSACTION_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=SOCIAL_TRANSACTION_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def social_transactions_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import SOCIAL_TRANSACTION_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=SOCIAL_TRANSACTION_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def commerce_payouts_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_PAYOUT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_PAYOUT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def commerce_payouts_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_PAYOUT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_PAYOUT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def social_payouts_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import SOCIAL_PAYOUT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=SOCIAL_PAYOUT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def social_payouts_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import SOCIAL_PAYOUT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=SOCIAL_PAYOUT_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def balances_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_BALANCE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_BALANCE_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def balances_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import COMMERCE_BALANCE_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=COMMERCE_BALANCE_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def activity_artists_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACTIVITY_ARTISTS_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACTIVITY_ARTISTS_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def activity_artists_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACTIVITY_ARTISTS_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACTIVITY_ARTISTS_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def activity_contents_added_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACTIVITY_CONTENTS_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACTIVITY_CONTENTS_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def activity_contents_updated_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACTIVITY_CONTENTS_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACTIVITY_CONTENTS_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def contents_publish_success_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PUBLISH_CONTENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PUBLISH_CONTENT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def contents_publish_failure_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PUBLISH_CONTENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PUBLISH_CONTENT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def contents_publish_ready_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PUBLISH_CONTENT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PUBLISH_CONTENT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def session_expired_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import ACCOUNT_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=ACCOUNT_TABLE_MAPPINGS, data=data)

    @classmethod
    async def user_created_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import USER_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=USER_TABLE_MAPPINGS, data=data)

    @classmethod
    async def sdk_token_created_event_handler(cls, data: Dict):
        pass

    @classmethod
    async def content_fetch_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import CONTENTS_INFORMATION_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=CONTENTS_INFORMATION_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def profile_analytics_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_ANALYTICS_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_ANALYTICS_TABLE_MAPPINGS, data=data)

    @classmethod
    async def profile_search_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_SEARCH_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_SEARCH_TABLE_MAPPINGS, data=data.get('data'))

    @classmethod
    async def profile_fetch_event_handler(cls, data: Dict):
        from app.events.db.mapper_config import PROFILE_FETCH_TABLE_MAPPINGS
        await cls.persist_to_db(table_mappings=PROFILE_FETCH_TABLE_MAPPINGS, data=data.get('data'))
