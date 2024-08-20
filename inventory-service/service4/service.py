import requests
from fastapi import HTTPException, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from service4 import setting
from service4.models.user_model import User
from service4.models.product_model import Product

oauth_scheme = OAuth2PasswordBearer(tokenUrl=f"{setting.USER_SERVICE_URL}/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]) -> User:
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
    response = requests.get(
        f"{setting.USER_SERVICE_URL}/auth/users/me", 
        headers={"Authorization": f"Bearer {token}"}
    )
    user = User(**response.json())
    if user is None:
        raise credentials_exception
    return user

def check_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Check if the user is an admin.
    Args:
        user (User): The user object.
    Returns:
        User: The user object.
    """
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized to perform this action")
    return user

def get_product(product_id: int) -> Product:
    """
    This fnction is used to get product from product service.
    Args:
        product_id (int): The id of the product to retrieve.
    Returns:
        dict: The product object.
    """
    response = requests.get(f"{setting.PRODUCT_SERVICE_URL}/product/{product_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found!")
    product = Product(**response.json())
    return product
