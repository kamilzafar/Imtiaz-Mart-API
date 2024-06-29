import random
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from service1.settings import *
from service1.models import *
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from fastapi import HTTPException, status
from pydantic import EmailStr
from typing import Union, Any
import requests
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    """
    Verify the password using the hash stored in the database.
    Args:
        plain_password (str): The password entered by the user.
        hashed_password (str): The password stored in the database.
    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash the password before storing it in the database.
    Args:
        password (str): The password entered by the user.
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def get_user_by_username(db:Session,username:str) -> User:
    """
    Get the user by username.
    Args:
        db (Session): The database session.
        username (str): The username of the user.
    Returns:
        User: The user object.
        """
    if username is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.exec(select(User).where(User.username == username)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def get_user_by_id(db: Session, userid: int) -> User:
    """
    Get the user by user id.
    Args:
        db (Session): The database session.
        userid (int): The user id.
    Returns:
        User: The user object.
        """
    if userid is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             headers={"WWW-Authenticate": 'Bearer'},
                             detail={"error": "invalid_token", "error_description": "The access token expired"})
    user = db.get(User, userid)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user
    
def get_user_by_email(db:Session,user_email: EmailStr) -> User:
    """
    Get the user by email.
    Args:
        db (Session): The database session.
        user_email (EmailStr): The email of the user.
    Returns:
        User: The user object.
    """
    if user_email is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.get(User, user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def authenticate_user(db, username: str, password: str) -> User:
    """
    Authenticate the user.
    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The password of the user.
    Returns:
        User: The user object.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create an access token.
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta): The time delta for the token to expire.
    Returns:
        str: The access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create a refresh token.
    Args:
        data (Union[str, Any]): The data to encode in the token.
        expires_delta (int): The time delta for the token to expire.
    Returns:
        str: The refresh token.
    """
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def add_consumer_to_kong(username: str):
    """
    Add a consumer to Kong.
    Args:
        username (str): The username of the consumer.
    Returns:
        dict: The response from Kong.
    """
    url = f"{KONG_ADMIN_URL}/consumers/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        # Consumer with the given username already exists, return it
        return response.json()
    
    url = f"{KONG_ADMIN_URL}/consumers"
    random_number = random.randint(10000, 99999)
    data = {"username": username, "custom_id": f"{random_number}"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,  data=json.dumps(data), headers=headers)

    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create consumer in Kong")

    consumer = response.json()

    # url = f"{KONG_ADMIN_URL}/consumers/{consumer['id']}/jwt"
    # jwt_data = {
    #     "algorithm": ALGORITHM,
    #     "key": "sub",
    #     "secret": SECRET_KEY
    # }
    # jwt_headers = {"Content-Type": "application/json"}
    # jwt_response = requests.post(url, json.dumps(jwt_data), headers=jwt_headers)

    # if jwt_response.status_code != 201:
    #     print(f"Failed to create JWT credential: {jwt_response.status_code} {jwt_response.text}")
    #     raise HTTPException(status_code=500, detail="Failed to create JWT credential for consumer")

    # jwt_credential = jwt_response.json()

    # consumer['jwt'] = jwt_credential
    return consumer

def delete_consumer_from_kong(username: str):
    """
    Delete a consumer from Kong.
    Args:
        username (str): The username of the consumer.
    Returns:
        dict: The response from Kong.
    """
    url = f"{KONG_ADMIN_URL}/consumers/{username}"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        raise HTTPException(status_code=500, detail="Failed to delete consumer from Kong")

    return {"message": "Consumer deleted successfully"}