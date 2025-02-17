from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.client import Base

if TYPE_CHECKING:
    from .customer import Customer
    from .product import Product

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity <= 10 and quantity > 0", name="check_quantity_range"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    
    # ManyToOne
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")