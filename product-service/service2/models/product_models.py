from typing import Optional
from uuid import UUID
from sqlmodel import Field, SQLModel, Column, Enum
import enum

class Category(str, enum.Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    category: Category = Field(default=Category.clothing, sa_column=Column("category", Enum(Category)))
    quantity: int

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID 

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(SQLModel):
    name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
