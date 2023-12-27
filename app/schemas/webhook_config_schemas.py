from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, constr, HttpUrl

class WebhookResponse(BaseModel):
    id: UUID
    name: constr(min_length=1, max_length=100, strip_whitespace=True)
    url: HttpUrl
    created_at: datetime
    updated_at: datetime
    is_active: bool
    events: Optional[List[str]]
