from uuid import uuid4
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from service1.settings import ALGORITHM, SECRET_KEY
from typing import List, Annotated
from jose import JWTError, jwt
from service1.db import db_session
from service1.models import *
from service1.services import *


def signup_user(user: UserCreate, db: Session) -> User:
    """
    Create a new user.
    Args:
        user (UserCreate): The user data.
        db (Session): The database session.
    Returns:
        User: The user object.
    """
    search_user_by_email = db.exec(select(User).where(User.email == user.email)).first()
    if search_user_by_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email id already registered")
    
    search_user_by_username = db.exec(select(User).where(User.username == user.username)).first()
    if search_user_by_username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Try Different username")
    
    hashed_password = get_password_hash(user.password)

    new_user = User(id = uuid4(), username=user.username, email=user.email, password=hashed_password, role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_session)]) -> User:
    """
    Get the current user.
    Args:
        token (str): The access token.
        db (Session): The database session.
    Returns:
        User: The user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def check_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Check if the user is an admin.
    Args:
        user (User): The user object.
    Returns:
        User: The user object.
    """
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not authorized to perform this action")
    return user
