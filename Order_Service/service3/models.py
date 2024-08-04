from typing import Optional
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

class OrderItem(SQLModel,table =True):
    id: int = Field(primary_key=True,default=None)
    order_id: int 
    user_id: UUID 
    product_id: int 
    price: int
    quantity: int

class OrderItemCreate(OrderBase):
    pass


class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    
class User(UserBase):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    role: UserRole = Field(default="user")


class CartBase(SQLModel):
    product_id: int
    quantity: int

class Cart(CartBase,table = True): 
    cart_id: int = Field(primary_key=True,default=None)
    user_id: UUID 
    product_total: int

class CartCreate(CartBase): 
    pass    

class CartUpdate(CartBase):
    pass

class CartRead(CartBase):
    cart_id: int
    user_id: UUID
    product_id: int

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: int
    category: Category
    image_id: int = Field()

class Product(ProductBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class InventoryBase(SQLModel):
    product_id: int
    quantity: int 

class Inventory(InventoryBase, table=True):
    inventory_id: int = Field(primary_key=True,default=None)
    inventory_name: str

class InventoryCreate(InventoryBase): 
    pass

class InventoryUpdate(SQLModel): 
   pass