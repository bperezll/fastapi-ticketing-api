from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Order, Customer
from db.client import get_db
from db.schemas.order import OrderSchema, OrderProductSchema

router = APIRouter(tags=["orders"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# List of orders made by a customer
@router.get("/", response_model=List[OrderProductSchema])
async def orders(customer_id: int, db: Session = Depends(get_db)):

    customer = db.get(Customer, customer_id)
    if customer is None or not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    query = select(Order).where(Order.customer_id == customer_id)
    results = db.execute(query).scalars().all()
    
    return results

# Order by id made by a customer
@router.get("/{id}", response_model=OrderProductSchema)
async def order(customer_id: int, id: int, db: Session = Depends(get_db)):

    customer = db.get(Customer, customer_id)
    if customer is None or not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found")

    query = select(Order).where(and_(Order.id == id, Order.customer_id == customer_id))
    result = db.execute(query).scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order not found")
    
    return result

# Add new order
@router.post("/", response_model=OrderProductSchema, status_code=status.HTTP_201_CREATED)
async def order(customer_id: int, order_schema: OrderSchema, db: Session = Depends(get_db)):
    
    if order_schema.quantity > 10 or order_schema.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantity must be between 1 and 10"
        )

    customer = db.execute(select(Customer).where(Customer.id == customer_id)).scalar_one_or_none()

    if customer is None or not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Customer is inactive or does not exist")

    # Convert schema into ORM model
    new_order = Order(
        quantity=order_schema.quantity,
        product_id=order_schema.product_id,
        customer_id=customer_id
    )

    db.add(new_order)

    try:
        db.commit()
        db.refresh(new_order)
        return new_order
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error creating order")
