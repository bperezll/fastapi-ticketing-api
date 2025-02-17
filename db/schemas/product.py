from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int | None = None
    name: str
    price: float
    description: str

    class Config:
        from_attributes = True
        extra = "forbid"

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "forbid"