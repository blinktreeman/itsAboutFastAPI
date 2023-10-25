from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from common.database import SessionLocal

from schemas.user import User, UserCreate
from repositories import user_repository

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=User)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return user_repository.create_user(db=db, created_user=user)


@router.get("/users/{user_id}", response_model=User)
def read(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=User)
def update(user: User, db: Session = Depends(get_db)):
    return user_repository.update_user(db, user)


@router.delete("/users/{user_id}", response_model=Response)
def delete(user_id: int, db: Session = Depends(get_db)):
    return user_repository.delete_user(db, user_id=user_id)
