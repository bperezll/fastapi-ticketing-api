from typing import Optional
from pydantic import BaseModel, EmailStr

class CustomerSchema(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    address: str
    country_code: str
    is_active: bool = True

    class Config:
        from_attributes = True
        extra = "forbid"

class CustomerUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    country_code: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "forbid"