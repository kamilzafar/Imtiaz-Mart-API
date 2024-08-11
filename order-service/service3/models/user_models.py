from enum import Enum
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field

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
