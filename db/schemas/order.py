from typing import Annotated
from pydantic import BaseModel, conint

from db.schemas.product import ProductSchema

class OrderSchema(BaseModel):
    id: int | None = None
    quantity: Annotated[int, conint(gt=0, le=10)]
    product_id: int

    class Config:
        from_attributes = True
        extra = "forbid"

class OrderProductSchema(BaseModel):
    id: int | None = None
    quantity: Annotated[int, conint(gt=0, le=10)]
    product: ProductSchema

    class Config:
        from_attributes = True
        extra = "forbid"