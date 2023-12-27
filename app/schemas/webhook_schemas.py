from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from app.schemas.enum import WebhookEvent


class WebhookPayload(BaseModel):
    account_id: str
    user_id: str
    last_updated_time: datetime


class WebhookRequestData(BaseModel):
    id: str
    event: WebhookEvent
    name: str
    data: Dict

    def __str__(self) -> str:
        return super().__str__()

    class Config:
        use_enum_values = True


class AccountConnectedEvent(WebhookPayload):
    pass


class ProfileEvent(WebhookPayload):
    profile_id: str


class ProfileAudienceEvent(WebhookPayload):
    profile_id: str


class ContentEvent(WebhookPayload):
    items: List = []


class ContentCommentEvent(WebhookPayload):
    items: List = []


class ContentGroupEvent(WebhookPayload):
    items: List = []


class TransactionEvent(WebhookPayload):
    items: List = []


class PayoutEvent(WebhookPayload):
    items: List = []


class BalanceEvent(WebhookPayload):
    items: List = []


class ActivityArtistEvent(WebhookPayload):
    items: List = []


class ActivityContentEvent(WebhookPayload):
    items: List = []


class PublishContentEvent(WebhookPayload):
    publish_id: str
