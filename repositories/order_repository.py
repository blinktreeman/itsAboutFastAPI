from fastapi import status
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from common import models
from schemas import order


def create_order(db: Session, created_order: order.OrderCreate):
    db.add(created_order)
    db.commit()
    db.refresh(created_order)
    return created_order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order(db: Session, updated_order: order.Order):
    db_order = db.query(models.Order).filter(models.Order.id == updated_order.id).first()
    update_data = updated_order.model_dump(exclude_unset=True)
    db.query(models.Order).filter(models.Order.id == updated_order.id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id)
    db_order.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
