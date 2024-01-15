import logging
from typing import Dict, Optional

from app.core.config import settings
from app.events.event_executor_registry import EventExecutorRegistry
from app.schemas.enum import WebhookEvent, Product, PlatformCategory
from app.schemas.webhook_schemas import WebhookRequestData, AccountConnectedEvent, ContentEvent, \
    ContentGroupEvent, ProfileEvent, TransactionEvent, PayoutEvent, BalanceEvent, ActivityArtistEvent, \
    ActivityContentEvent, ProfileAudienceEvent, ContentCommentEvent, PublishContentEvent
from app.services.resource_service import fetch_contents_by_ids, fetch_account_by_id, fetch_content_groups_by_ids, \
    fetch_profile_by_id, fetch_social_transactions_by_ids, fetch_social_payouts_by_ids, fetch_balances_by_ids, \
    fetch_activity_artists_by_ids, fetch_activity_contents_by_ids, fetch_profile_audience_by_account_id, \
    fetch_content_comments_by_content_id_account_id, fetch_commerce_transactions_by_ids, fetch_commerce_payouts_by_ids, \
    fetch_publish_content_by_id


async def process_webhook(webhook_request_data: WebhookRequestData):
    if webhook_request_data.event == WebhookEvent.ACCOUNTS_CONNECTED \
            or webhook_request_data.event == WebhookEvent.ACCOUNTS_DISCONNECTED \
            or webhook_request_data.event == WebhookEvent.SESSION_EXPIRED:
        await add_update_account(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.PROFILES_ADDED
          or webhook_request_data.event == WebhookEvent.PROFILES_UPDATED) \
            and Product.IDENTITY in settings.SUPPORTED_PRODUCTS:
        await add_update_profile(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.PROFILES_AUDIENCE_ADDED
          or webhook_request_data.event == WebhookEvent.PROFILES_AUDIENCE_UPDATED) \
            and Product.IDENTITY_AUDIENCE in settings.SUPPORTED_PRODUCTS:
        await add_update_profile_audience(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.CONTENTS_ADDED
          or webhook_request_data.event == WebhookEvent.CONTENTS_UPDATED) \
            and Product.ENGAGEMENT in settings.SUPPORTED_PRODUCTS:
        await add_update_contents(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.CONTENTS_COMMENTS_ADDED
          or webhook_request_data.event == WebhookEvent.CONTENTS_COMMENTS_UPDATED) \
            and Product.ENGAGEMENT_AUDIENCE in settings.SUPPORTED_PRODUCTS:
        await add_update_content_comments(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.CONTENT_GROUPS_ADDED
          or webhook_request_data.event == WebhookEvent.CONTENT_GROUPS_UPDATED) \
            and Product.ENGAGEMENT in settings.SUPPORTED_PRODUCTS:
        await add_update_content_groups(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.TRANSACTIONS_ADDED
          or webhook_request_data.event == WebhookEvent.TRANSACTIONS_UPDATED) \
            and Product.INCOME in settings.SUPPORTED_PRODUCTS:
        await add_update_transactions(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.PAYOUTS_ADDED
          or webhook_request_data.event == WebhookEvent.PAYOUTS_UPDATED) \
            and Product.INCOME in settings.SUPPORTED_PRODUCTS:
        await add_update_payouts(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.BALANCES_ADDED
          or webhook_request_data.event == WebhookEvent.BALANCES_UPDATED) \
            and Product.INCOME in settings.SUPPORTED_PRODUCTS:
        await add_update_balances(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.ACTIVITY_ARTISTS_ADDED
          or webhook_request_data.event == WebhookEvent.ACTIVITY_ARTISTS_UPDATED) \
            and Product.ACTIVITY in settings.SUPPORTED_PRODUCTS:
        await add_update_activity_artists(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.ACTIVITY_CONTENTS_ADDED
          or webhook_request_data.event == WebhookEvent.ACTIVITY_CONTENTS_UPDATED) \
            and Product.ACTIVITY in settings.SUPPORTED_PRODUCTS:
        await add_update_activity_contents(webhook_request_data=webhook_request_data)

    elif (webhook_request_data.event == WebhookEvent.CONTENTS_PUBLISH_READY
          or webhook_request_data.event == WebhookEvent.CONTENTS_PUBLISH_SUCCESS
          or webhook_request_data.event == WebhookEvent.CONTENTS_PUBLISH_FAILURE) \
            and Product.PUBLISH_CONTENT in settings.SUPPORTED_PRODUCTS:
        await add_update_publish_content(webhook_request_data=webhook_request_data)


async def send_events(webhook_event: WebhookEvent, data: Dict, category: Optional[PlatformCategory] = None):
    for executor_event in EventExecutorRegistry.get_all_events():
        if webhook_event == WebhookEvent.ACCOUNTS_CONNECTED:
            await executor_event.accounts_connected_event_handler(data=data)
        elif webhook_event == WebhookEvent.ACCOUNTS_DISCONNECTED:
            await executor_event.accounts_disconnected_event_handler(data=data)
        elif webhook_event == WebhookEvent.PROFILES_ADDED:
            await executor_event.profiles_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.PROFILES_UPDATED:
            await executor_event.profiles_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.PROFILES_AUDIENCE_ADDED:
            await executor_event.profiles_audience_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.PROFILES_AUDIENCE_UPDATED:
            await executor_event.profiles_audience_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_ADDED:
            await executor_event.contents_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_UPDATED:
            await executor_event.contents_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_COMMENTS_ADDED:
            await executor_event.content_comments_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_COMMENTS_UPDATED:
            await executor_event.content_comments_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENT_GROUPS_ADDED:
            await executor_event.content_groups_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENT_GROUPS_UPDATED:
            await executor_event.content_groups_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.TRANSACTIONS_ADDED and category == PlatformCategory.COMMERCE:
            await executor_event.commerce_transactions_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.TRANSACTIONS_UPDATED and category == PlatformCategory.COMMERCE:
            await executor_event.commerce_transactions_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.TRANSACTIONS_ADDED and category == PlatformCategory.SOCIAL:
            await executor_event.social_transactions_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.TRANSACTIONS_UPDATED and category == PlatformCategory.SOCIAL:
            await executor_event.social_transactions_updated_event_handler(data=data)

        elif webhook_event == WebhookEvent.PAYOUTS_ADDED and category == PlatformCategory.COMMERCE:
            await executor_event.commerce_payouts_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.PAYOUTS_UPDATED and category == PlatformCategory.COMMERCE:
            await executor_event.commerce_payouts_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.PAYOUTS_ADDED and category == PlatformCategory.SOCIAL:
            await executor_event.social_payouts_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.PAYOUTS_UPDATED and category == PlatformCategory.SOCIAL:
            await executor_event.social_payouts_updated_event_handler(data=data)

        elif webhook_event == WebhookEvent.BALANCES_ADDED:
            await executor_event.balances_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.BALANCES_UPDATED:
            await executor_event.balances_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.ACTIVITY_ARTISTS_ADDED:
            await executor_event.activity_artists_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.ACTIVITY_ARTISTS_UPDATED:
            await executor_event.activity_artists_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.ACTIVITY_CONTENTS_ADDED:
            await executor_event.activity_contents_added_event_handler(data=data)
        elif webhook_event == WebhookEvent.ACTIVITY_CONTENTS_UPDATED:
            await executor_event.activity_contents_updated_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_PUBLISH_SUCCESS:
            await executor_event.contents_publish_success_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_PUBLISH_FAILURE:
            await executor_event.contents_publish_failure_event_handler(data=data)
        elif webhook_event == WebhookEvent.CONTENTS_PUBLISH_READY:
            await executor_event.contents_publish_ready_event_handler(data=data)
        elif webhook_event == WebhookEvent.SESSION_EXPIRED:
            await executor_event.session_expired_event_handler(data=data)


async def add_update_account(webhook_request_data: WebhookRequestData):
    account_connected_event: AccountConnectedEvent = AccountConnectedEvent(**webhook_request_data.data)

    if not account_connected_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    account: Dict = await fetch_account_by_id(account_id=account_connected_event.account_id)

    if not account:
        logging.error(f"Account does not exists with account_id: {account_connected_event.account_id}")
        return

    await send_events(webhook_request_data.event, data=account)


async def add_update_profile(webhook_request_data: WebhookRequestData):
    profile_event: ProfileEvent = ProfileEvent(**webhook_request_data.data)

    if not profile_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    profile: Dict = await fetch_profile_by_id(profile_id=profile_event.profile_id)

    if not profile:
        logging.error(f"Profile does not exists with profile_id: {profile_event.profile_id}")
        return

    await send_events(webhook_request_data.event, data=profile)


async def add_update_profile_audience(webhook_request_data: WebhookRequestData):
    profile_audience_event: ProfileAudienceEvent = ProfileAudienceEvent(**webhook_request_data.data)

    if not profile_audience_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    profile_audience: Dict = await fetch_profile_audience_by_account_id(account_id=profile_audience_event.account_id)

    if not profile_audience:
        logging.error(f"Profile-Audience does not exists with profile_audience_id: {profile_audience_event.profile_id}")
        return

    await send_events(webhook_request_data.event, data=profile_audience)


async def add_update_contents(webhook_request_data: WebhookRequestData):
    content_added_event: ContentEvent = ContentEvent(**webhook_request_data.data)

    if not content_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if content_added_event.items:
        contents: Dict = await fetch_contents_by_ids(ids=content_added_event.items)

        if not contents:
            logging.error(f"Contents does not exists with content-ids: {content_added_event.items}")
            return

        await send_events(webhook_request_data.event, data=contents)


async def add_update_content_comments(webhook_request_data: WebhookRequestData):
    content_comment_added_event: ContentCommentEvent = ContentCommentEvent(**webhook_request_data.data)

    if not content_comment_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if content_comment_added_event.items:
        limit: int = 100
        for content_id in content_comment_added_event.items:
            offset: int = 0
            while True:
                content_comments: Dict = await fetch_content_comments_by_content_id_account_id(
                    content_id=content_id, account_id=content_comment_added_event.account_id,
                    limit=limit, offset=offset)

                if not content_comments and offset == 0:
                    logging.error(f"Content-Comments does not exists with content-id: {content_id}")
                    break

                await send_events(webhook_event=webhook_request_data.event, data=content_comments)

                if len(content_comments) < limit:
                    break
                else:
                    offset += limit


async def add_update_content_groups(webhook_request_data: WebhookRequestData):
    content_group_added_event: ContentGroupEvent = ContentGroupEvent(**webhook_request_data.data)

    if not content_group_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if content_group_added_event.items:
        content_groups: Dict = await fetch_content_groups_by_ids(ids=content_group_added_event.items)

        if not content_groups:
            logging.error(f"Content-groups does not exists with content-group-ids: {content_group_added_event.items}")
            return

        await send_events(webhook_event=webhook_request_data.event, data=content_groups)


async def add_update_transactions(webhook_request_data: WebhookRequestData):
    transaction_added_event: TransactionEvent = TransactionEvent(**webhook_request_data.data)

    if not transaction_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if transaction_added_event.items:
        category = await _get_work_platform_category_by_account_id(account_id=transaction_added_event.account_id)
        if category == PlatformCategory.COMMERCE:
            await _add_update_commerce_transaction(webhook_event=webhook_request_data.event,
                                                   transaction_event=transaction_added_event)
        else:
            await _add_update_social_transaction(webhook_event=webhook_request_data.event,
                                                 transaction_event=transaction_added_event)


async def _add_update_social_transaction(webhook_event: WebhookEvent, transaction_event: TransactionEvent):
    if transaction_event.items:
        transactions: Dict = await fetch_social_transactions_by_ids(ids=transaction_event.items)

        if not transactions:
            logging.error(f"Transaction does not exists with transaction-ids: {transaction_event.items}")
            return

        await send_events(webhook_event=webhook_event, data=transactions, category=PlatformCategory.SOCIAL)


async def _add_update_commerce_transaction(webhook_event: WebhookEvent, transaction_event: TransactionEvent):
    if transaction_event.items:
        transactions: Dict = await fetch_commerce_transactions_by_ids(ids=transaction_event.items)

        if not transactions:
            logging.error(f"Commerce-Transaction does not exists with transaction-ids: {transaction_event.items}")
            return

        await send_events(webhook_event=webhook_event, data=transactions, category=PlatformCategory.COMMERCE)


async def add_update_payouts(webhook_request_data: WebhookRequestData):
    payouts_added_event: PayoutEvent = PayoutEvent(**webhook_request_data.data)

    if not payouts_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if payouts_added_event.items:
        category = await _get_work_platform_category_by_account_id(account_id=payouts_added_event.account_id)
        if category == PlatformCategory.COMMERCE:
            await _add_update_commerce_payout(webhook_event=webhook_request_data.event,
                                              payouts_event=payouts_added_event)
        else:
            await _add_update_social_payout(webhook_event=webhook_request_data.event,
                                            payouts_event=payouts_added_event)


async def _add_update_social_payout(webhook_event: WebhookEvent, payouts_event: PayoutEvent):
    if payouts_event.items:
        payouts: Dict = await fetch_social_payouts_by_ids(ids=payouts_event.items)

        if not payouts:
            logging.error(f"Social-Payout does not exists with payout-ids: {payouts_event.items}")
            return

        await send_events(webhook_event=webhook_event, data=payouts, category=PlatformCategory.SOCIAL)


async def _add_update_commerce_payout(webhook_event: WebhookEvent, payouts_event: PayoutEvent):
    if payouts_event.items:
        payouts: Dict = await fetch_commerce_payouts_by_ids(ids=payouts_event.items)

        if not payouts:
            logging.error(f"Commerce-Payout does not exists with payout-ids: {payouts_event.items}")
            return
        await send_events(webhook_event=webhook_event, data=payouts, category=PlatformCategory.COMMERCE)


async def add_update_balances(webhook_request_data: WebhookRequestData):
    balances_added_event: BalanceEvent = BalanceEvent(**webhook_request_data.data)

    if not balances_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if balances_added_event.items:
        balances: Dict = await fetch_balances_by_ids(ids=balances_added_event.items)

        if not balances:
            logging.error(f"Balance does not exists with balance-ids: {balances_added_event.items}")
            return
        await send_events(webhook_event=webhook_request_data.event, data=balances)


async def add_update_activity_artists(webhook_request_data: WebhookRequestData):
    activity_artists_added_event: ActivityArtistEvent = ActivityArtistEvent(**webhook_request_data.data)

    if not activity_artists_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if activity_artists_added_event.items:
        activity_artists: Dict = await fetch_activity_artists_by_ids(ids=activity_artists_added_event.items)

        if not activity_artists:
            logging.error(f"Activity-Artist does not exists with "
                          f"activity-artist-ids: {activity_artists_added_event.items}")
            return

        await send_events(webhook_event=webhook_request_data.event, data=activity_artists)


async def add_update_activity_contents(webhook_request_data: WebhookRequestData):
    activity_contents_added_event: ActivityContentEvent = ActivityContentEvent(**webhook_request_data.data)

    if not activity_contents_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if activity_contents_added_event.items:
        activity_contents: Dict = await fetch_activity_contents_by_ids(ids=activity_contents_added_event.items)

        if not activity_contents:
            logging.error(f"Activity-Content does not exists with "
                          f"activity-content-ids: {activity_contents_added_event.items}")
            return

        await send_events(webhook_event=webhook_request_data.event, data=activity_contents)


async def add_update_publish_content(webhook_request_data: WebhookRequestData):
    publish_contents_added_event: PublishContentEvent = PublishContentEvent(**webhook_request_data.data)

    if not publish_contents_added_event:
        logging.info(f"Empty body for webhook-id: {webhook_request_data.id}")
        return

    if publish_contents_added_event.publish_id:
        publish_content: Dict = await fetch_publish_content_by_id(id=publish_contents_added_event.publish_id)

        if not publish_content:
            logging.error(f"Publish-Content does not exists with publish-id: {publish_contents_added_event.publish_id}")
            return

        await send_events(webhook_event=webhook_request_data.event, data=publish_content)


async def _get_work_platform_category_by_account_id(account_id: str):
    response: Dict = await fetch_account_by_id(account_id=account_id)
    if response:
        work_platform_name: str = response.get('work_platform', {}).get('name')
        if work_platform_name.upper() in ('SHOPIFY', 'ETSY', 'STRIPE', 'GUMROAD', 'FBCOMMERCE'):
            return PlatformCategory.COMMERCE
        else:
            return PlatformCategory.SOCIAL
