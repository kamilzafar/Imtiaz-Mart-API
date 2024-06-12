from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID
from datetime import timedelta

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: timedelta

class TokenData(SQLModel):
    username: str

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

class Userlogin(UserBase):
    pass

class UserUpdate(SQLModel):
    username: str

class User(UserBase, table=True):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)

class UserCreate(UserBase):
    email: str