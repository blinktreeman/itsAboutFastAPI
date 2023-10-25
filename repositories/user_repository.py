from sqlalchemy.orm import Session

from common import models
from schemas import user


def create_user(db: Session, created_user: user.UserCreate):
    # TODO: hash
    fake_hashed_password = created_user.password + "fake_hashed"
    db_user = models.User(first_name=created_user.first_name,
                          last_name=created_user.last_name,
                          email=created_user.email,
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

