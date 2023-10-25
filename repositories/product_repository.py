from fastapi import status
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from common import models
from schemas import product


def create_product(db: Session, created_product: product.ProductCreate):
    db.add(created_product)
    db.commit()
    db.refresh(created_product)
    return created_product


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, updated_product: product.Product):
    db_product = db.query(models.Product).filter(models.Product.id == updated_product.id).first()
    update_data = updated_product.model_dump(exclude_unset=True)
    db.query(models.Product).filter(models.Product.id == updated_product.id).update(update_data,
                                                                                    synchronize_session=False)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id)
    db_product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
