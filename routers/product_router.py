from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from common.database import SessionLocal

from schemas.product import Product, ProductCreate
from repositories import product_repository

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/products/", response_model=Product)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return product_repository.create_product(db=db, created_product=product)


@router.get("/products/{product_id}", response_model=Product)
def read(product_id: int, db: Session = Depends(get_db)):
    db_product = product_repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_product


@router.put("/products/{product_id}", response_model=Product)
def update(product: Product, db: Session = Depends(get_db)):
    return product_repository.update_product(db, product)


@router.delete("/products/{product_id}", response_model=Response)
def delete(product_id: int, db: Session = Depends(get_db)):
    return product_repository.delete_product(db, product_id=product_id)
