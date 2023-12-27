import logging
import urllib.parse
from pydoc import locate
from typing import Dict, List, Set

from starlette.datastructures import CommaSeparatedStrings

from app.core.config import settings
from app.events.event_executor_registry import EventExecutorRegistry
from app.schemas.enum import WebhookEvent
from app.schemas.webhook_config_schemas import WebhookResponse
from app.services.resource_service import fetch_all_webhooks, create_webhook, update_webhook
from app.utils.validator import get_supported_webhook_events


async def configure_webhooks():
    existing_webhooks: Dict = await fetch_all_webhooks()

    webhook_url = urllib.parse.urljoin(settings.WEBHOOK_BASE_URL, "/v1/webhook/process")
    events: Set[WebhookEvent] = get_supported_webhook_events()

    webhook_exists: bool = False
    if existing_webhooks and existing_webhooks.get('data'):
        data: List[Dict] = existing_webhooks.get('data')
        for webhook in data:
            webhook_response: WebhookResponse = WebhookResponse(**webhook)
            if webhook_response.url == webhook_url:
                webhook_exists = True
                logging.info(f"URL is already configured for events: {webhook_response.events}")

                #  Validate webhook is configured for supported products or not. If not, then register the events
                if not webhook_response.is_active:
                    await update_webhook(id=webhook_response.id, name=webhook_response.name,
                                         webhook_url=webhook_url, events=list(events))
                    break

                for event in events:
                    if event not in webhook_response.events:
                        await update_webhook(id=webhook_response.id, name=webhook_response.name,
                                             webhook_url=webhook_url, events=list(events))
                        break
                break

    if not webhook_exists:
        await create_webhook(webhook_url=webhook_url, events=list(events))


async def register_event_listeners(event_executors: CommaSeparatedStrings):
    # Configure all the event-executors which needs to be registered over here

    if event_executors:
        for event_executor in event_executors:
            EventExecutorRegistry.register(identifier="1", executor_class=locate(event_executor))
