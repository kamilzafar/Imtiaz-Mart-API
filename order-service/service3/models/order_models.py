from uuid import UUID
from sqlmodel import SQLModel,Field
from enum import Enum

class OrderStatus(str,Enum):
    PENDING: str = "pending"
    CANCELLED: str = "cancelled"
    DELIVERED: str = "delivered"
    PAID: str = "paid"

class OrderBase(SQLModel):
    username: str
    email: str
    address: str
    contactnumber: str
    city: str

class Order(OrderBase, table = True):
    order_id: int = Field(primary_key=True,default=None)
    user_id: UUID 
    total_price: int
    order_status: OrderStatus = Field(default="pending")

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    order_status: OrderStatus

class OrderRead(OrderBase):
    pass

class OrderItem(SQLModel, table = True):
    id: int = Field(primary_key=True,default=None)
    order_id: int 
    user_id: UUID 
    product_id: int 
    price: int
    quantity: int

class OrderItemCreate(OrderBase):
    pass
