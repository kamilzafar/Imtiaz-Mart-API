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

class User(UserBase):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)
    role: UserRole = Field(default=UserRole.user, sa_column=Column("role", Enum(UserRole)))