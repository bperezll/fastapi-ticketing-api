from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.client import Base

if TYPE_CHECKING:
    from .order import Order

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    price: Mapped[float]
    description: Mapped[str] = mapped_column(String(200), unique=True)

    # OneToMany
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")