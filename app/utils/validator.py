from typing import Set

from starlette.datastructures import CommaSeparatedStrings

from app.core.config import settings
from app.schemas.enum import Product, WebhookEvent, product_webhook_event_mapping


def validate_products(products: CommaSeparatedStrings):
    [Product(p) for p in products]


def get_supported_webhook_events() -> Set:
    products = settings.SUPPORTED_PRODUCTS
    events: Set[WebhookEvent] = set()

    for p in products:
        events = events.union(product_webhook_event_mapping.get(p))

    events.add(WebhookEvent.ACCOUNTS_CONNECTED)
    events.add(WebhookEvent.ACCOUNTS_DISCONNECTED)
    events.add(WebhookEvent.SESSION_EXPIRED)
    return events
