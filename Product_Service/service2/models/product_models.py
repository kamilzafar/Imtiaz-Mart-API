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
    price: int
    category: Category = Field(default=Category.clothing, sa_column=Column("category", Enum(Category)))

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID 

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass
