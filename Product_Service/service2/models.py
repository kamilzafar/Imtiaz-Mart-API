from sqlmodel import SQLModel, Field, Column, Enum
from typing import Optional
from uuid import UUID
import enum

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    filename: str
    content_type: str
    image_data: bytes

class Category(str, enum.Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: int
    stock: int
    category: Category = Field(default=Category.clothing,sa_column=Column("category", Enum(Category)))
    image_id: int = Field(foreign_key="image.id")

class Product(ProductBase, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True, index=True)

class ProductRead(ProductBase):
    id: UUID

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass