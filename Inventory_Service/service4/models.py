from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from uuid import UUID

class InventoryBase(SQLModel):
    product_id: int
    quantity: int 

class Inventory(InventoryBase, table=True):
    inventory_id: int = Field(primary_key=True,default=None)
    inventory_name: str

class InventoryCreate(InventoryBase):
    inventory_name: str

class InventoryUpdate(InventoryBase):
    pass

class InventoryDelete(SQLModel):
    product_id: int

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