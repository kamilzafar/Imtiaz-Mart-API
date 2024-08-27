from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel,Field,Column, Enum
import enum


class OrderStatus(str, enum.Enum):
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

class Order(OrderBase):
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

class OrderItem(SQLModel):
    id: int = Field(primary_key=True,default=None)
    order_id: int 
    user_id: UUID 
    product_id: int 
    price: int
    quantity: int

class OrderItemCreate(OrderBase):
    pass

class Category(str, enum.Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: int
    category: Category = Field(default=Category.clothing, sa_column=Column("category", Enum(Category)))

class Product(ProductBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class User(SQLModel):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="user")