from typing import List
from uuid import UUID

from pydantic import BaseModel, constr, validator

from app.core.config import settings
from app.schemas.enum import Product
from app.utils.validator import validate_products


class UserRequest(BaseModel):
    name: constr(min_length=1, max_length=100, strip_whitespace=True)
    external_id: constr(min_length=1, max_length=100, strip_whitespace=True)


class SdkTokenRequest(BaseModel):
    user_id: UUID
    products: List[str] = []

    @validator('products', pre=True, always=True)
    def validate_products(cls, products):
        if products:
            validate_products(products)
        else:
            products = [Product(p).value for p in settings.SUPPORTED_PRODUCTS._items]
        return products
