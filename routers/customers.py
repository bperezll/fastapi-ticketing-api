from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.client import get_db
from db.models import Customer
from db.schemas.customer import CustomerSchema, CustomerUpdateSchema

router = APIRouter(prefix="/customers", 
            tags=["customers"], 
            responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# List of all active customers
@router.get("/", response_model=List[CustomerSchema])
async def customers(db: Session = Depends(get_db)):

    query = select(Customer).where(Customer.is_active == True)
    results = db.execute(query).scalars().all()
    
    return results

# List of inactive customers
@router.get("/inactive", response_model=List[CustomerSchema])
async def customers(db: Session = Depends(get_db)):

    query = select(Customer).where(Customer.is_active == False)
    inactive_customers = db.execute(query).scalars().all()

    return inactive_customers

# Customer by id
@router.get("/{id}", response_model=CustomerSchema)
async def customer(id: int, db: Session = Depends(get_db)):

    query = select(Customer).where(and_(Customer.id == id, Customer.is_active == True))
    result = db.execute(query).scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer not found")
    
    return result

# Add new customer
@router.post("/", response_model=CustomerSchema, status_code=status.HTTP_201_CREATED)
async def customer(customer_schema: CustomerSchema, db: Session = Depends(get_db)):
    
    # Convert schema into ORM model
    new_customer = Customer(
        name=customer_schema.name,
        email=customer_schema.email,
        address=customer_schema.address,
        country_code=customer_schema.country_code,
    )

    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error creating customer: unique constraint violated")

# Edit customer by id
@router.put("/{id}", response_model=CustomerSchema)
async def customer(id: int, customer_schema: CustomerUpdateSchema, db: Session = Depends(get_db)):

    customer = db.get(Customer, id)

    if customer is None or not customer.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    update_data = customer_schema.model_dump(exclude_unset=True)

    update_data.pop("is_active", None)

    for field, value in update_data.items():
        setattr(customer, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating customer: unique constraint violated"
        )
    
    db.refresh(customer)

    return customer

# Restore an inactive customer
@router.put("/{id}/restore", response_model=CustomerSchema)
async def customer(id: int, db: Session = Depends(get_db)):

    customer = db.get(Customer, id)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    if customer.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer is already active")

    customer.is_active = True
    db.commit()
    db.refresh(customer)

    return customer

# Soft delete of a customer by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def customer(id: int, db: Session = Depends(get_db)):

    query = select(Customer).where(Customer.id == id)
    result = db.execute(query).scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    result.is_active = False
    db.commit()