from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel,Field
from enum import Enum
from datetime import timedelta

class Size(str,Enum):
    LARGE:str = "large"
    SMALL:str = "small"
    MEDIUM:str = "medium"

class OrderStatus(str,Enum):
    PENDING:str = "pending"
    CANCELLED:str = "cancelled"
    DELIVERED:str = "delivered"

class OrderBase(SQLModel):
    order_status:OrderStatus
    customer_name:str
    customer_email:str


class Order(OrderBase,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(SQLModel):
    order_status:OrderStatus

class OrderRead(OrderBase):
    pass

class OrderItemBase(SQLModel):
    total_cart_products:int
    product_total:int
    product_size:Size

class OrderItem(OrderItemBase,table =True):
    orderitem_id:int | None = Field(primary_key=True,default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None)

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
    product_size:Size

class Cart(CartBase,table = True):
    cart_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None) 

class CartCreate(CartBase):
    pass    

class CartUpdate(CartBase):
    pass

class CartRead(CartBase):
    cart_id:int
    user_id:int
    product_id:int

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: timedelta

class TokenData(SQLModel):
    username: str