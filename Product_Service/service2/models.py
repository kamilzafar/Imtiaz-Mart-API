from sqlmodel import SQLModel, Field, Column, Enum
from typing import Optional
from uuid import UUID
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

class User(UserBase, table=True):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    role: UserRole = Field(default=UserRole.user, sa_column=Column("role", Enum(UserRole)))

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
    category: Category = Field(default=Category.clothing,sa_column=Column("category", Enum(Category)))
    image_id: int = Field(foreign_key="image.id")

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class TokenData(SQLModel):
    username: str