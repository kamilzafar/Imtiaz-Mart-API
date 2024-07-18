from sqlmodel import SQLModel,Field,Column
from enum import Enum
from uuid import UUID
from datetime import timedelta

class InventoryBase(SQLModel):
    inventory_name:str
    inventory_description:str
    quantity:int 

class Inventory(InventoryBase,table=True):
    inventory_id:int | None = Field(primary_key=True,default=None)
    product_id:int | None = Field(foreign_key="product.id",default=None)
    user_id:UUID | None = Field(foreign_key="user.id",default=None)

class InventoryCreate(InventoryBase):
    product_id:int | None

class InventoryUpdate(SQLModel):
    quantity:int 

class InventoryRead(InventoryBase):
    pass

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    
class User(UserBase, table=True):
    id: UUID | None = Field(primary_key=True, index=True,default=None)

class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
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
    category: Category
    image_id: int = Field(foreign_key="image.id")
    

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

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