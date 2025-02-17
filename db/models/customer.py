from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.client import Base

if TYPE_CHECKING:
    from .order import Order

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    address: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    # OneToMany
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="customer")