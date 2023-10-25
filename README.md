# It's about FastAPI

Задание:
> Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
> 1. Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
> 2. Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
> 3. Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
> - Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
> - Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
> - Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.  
> 
> Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
> Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API

## Реализация

### Определим конфигурацию

settings.py

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = '.env'


settings = Settings()
```

### Соединение с СУБД

database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```
### Описываем модели БД
```python
from sqlalchemy import String, Integer, Float, Date, ForeignKey, Column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(Date, nullable=False)
    status = Column(String(25))
```
### Описываем схемы сущностей
 Для User (user.py):
 ```python
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
```
### Репозиторий для User
Реализация CRUD user_repository.py:
```python
from fastapi import status
from fastapi.openapi.models import Response
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


def update_user(db: Session, updated_user: user.User):
    db_user = db.query(models.User).filter(models.User.id == updated_user.id).first()
    update_data = updated_user.model_dump(exclude_unset=True)
    db.query(models.User).filter(models.User.id == updated_user.id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    db_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
### Routing
Для User (user_router.py):
```python
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
```

Аналогично для сущностей Product, Order

## Main файл

```python
from fastapi import FastAPI

from common.database import engine
from common import models
from routers import user_router, product_router, order_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_router.router, tags=["users"])
app.include_router(product_router.router, tags=["products"])
app.include_router(order_router.router, tags=["orders"])
```
