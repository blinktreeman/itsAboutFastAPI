from pydantic import BaseModel
from enum import Enum
import datetime


class Status(Enum):
    placed = 'размещен',
    paid = 'оплачен'
    completed = 'выполнен'


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime.date
    status: Status

    class Config:
        use_enum_values = True


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
