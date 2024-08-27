from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from uuid import UUID

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"

class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    category: Category
    quantity: int

class Product(ProductBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass