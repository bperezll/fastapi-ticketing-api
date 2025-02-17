from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.client import get_db
from db.models import Product
from db.schemas.product import ProductSchema, ProductUpdateSchema

router = APIRouter(prefix="/products", 
                   tags=["products"], 
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

# List of all products
@router.get("/", response_model=List[ProductSchema])
async def products(db: Session = Depends(get_db)):

    query = select(Product)
    results = db.execute(query).scalars().all()

    return results

# Product by id
@router.get("/{id}", response_model=ProductSchema)
async def product(id: int, db: Session = Depends(get_db)):

    query = select(Product).where(Product.id == id)
    result = db.execute(query).scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")
    
    return result

# Add new product
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def product(product_schema: ProductSchema, db: Session = Depends(get_db)):
    
    # Convert schema into ORM model
    new_product = Product(
        name=product_schema.name,
        price=product_schema.price,
        description=product_schema.description,
    )

    db.add(new_product)

    try:
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error updating product: unique constraint violated")

# Edit product by id
@router.put("/{id}", response_model=ProductSchema)
async def product(id: int, product_schema: ProductUpdateSchema, db: Session = Depends(get_db)):

    product = db.get(Product, id)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    update_data = product_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating product: unique constraint violated"
        )
    
    db.refresh(product)

    return product