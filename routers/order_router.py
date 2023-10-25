from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from common.database import SessionLocal

from schemas.order import Order, OrderCreate
from repositories import order_repository
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/orders/", response_model=Order)
def create(order: OrderCreate, db: Session = Depends(get_db)):
    return order_repository.create_order(db=db, created_order=order)


@router.get("/orders/{order_id}", response_model=Order)
def read(order_id: int, db: Session = Depends(get_db)):
    db_order = order_repository.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.put("/orders/{order_id}", response_model=Order)
def update(order: Order, db: Session = Depends(get_db)):
    return order_repository.update_order(db, order)


@router.delete("/orders/{order_id}", response_model=Response)
def delete(order_id: int, db: Session = Depends(get_db)):
    return order_repository.delete_order(db, order_id=order_id)
