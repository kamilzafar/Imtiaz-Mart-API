from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel,Field,Column
from enum import Enum
from datetime import timedelta



class OrderStatus(str,Enum):
    PENDING:str = "pending"
    CANCELLED:str = "cancelled"
    DELIVERED:str = "delivered"
    PAID:str = "paid"

class OrderBase(SQLModel):
    customer_name:str
    customer_email:str
    customer_address:str
    customer_phoneno:str
    customer_city:str

class Order(OrderBase,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    user_id:UUID | None = Field(foreign_key="user.id",default=None)
    order_status:OrderStatus


class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    order_status:OrderStatus

class OrderRead(OrderBase):
    pass

class OrderItemBase(SQLModel):
    total_cart_products:int
    product_total:int

class OrderItem(OrderItemBase,table =True):
    orderitem_id:int | None = Field(primary_key=True,default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:UUID | None = Field(foreign_key="user.id",default=None)
    product_id:int | None = Field(foreign_key="product.id",default=None)

class OrderItemCreate(OrderBase):
    pass

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    
class User(UserBase, table=True):
    id: Optional[UUID] = Field(primary_key=True, index=True)

class CartBase(SQLModel):
    total_cart_products:int
    product_total:int

class Cart(CartBase,table = True):
    cart_id:int | None = Field(primary_key=True,default=None)
    user_id:UUID | None = Field(foreign_key="user.id",default=None)
    product_id:int | None = Field(foreign_key="product.id",default=None) 

class CartCreate(CartBase):
    pass    

class CartUpdate(CartBase):
    pass

class CartRead(CartBase):
    cart_id:int
    user_id:UUID
    product_id:int

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: timedelta

class TokenData(SQLModel):
    username: str


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    filename: str
    content_type: str
    image_data: bytes

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: int
    stock: int
    category: Category
    image_id: int = Field(foreign_key="image.id")

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID | None = Field(foreign_key="user.id")

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass