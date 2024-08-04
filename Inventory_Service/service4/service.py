import requests
from sqlmodel import Session,select
from service4.models import *
from service4.database import *
from fastapi import HTTPException, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from service4 import setting
from jose import jwt, JWTError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

def service_get_inventory(db: Session, product_id: int) -> Inventory:
    """
    This function is used to get inventory by product id.
    Args:
        db (Session): The database session.
        product_id (int): The id of the product.
    Returns:
        dict: The inventory object.
    """
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    inventory = db.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory Not Found")
    return inventory
    
def service_create_inventory(db: Session, inventory_data: InventoryCreate) -> Inventory:
    """
    This function is used to create inventory.
    Args:
        db (Session): The database session.
        inventory_data (InventoryCreate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory_data = Inventory(
        inventory_name=inventory_data.inventory_name,
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity,
    )
    db.add(inventory_data)
    db.commit()
    db.refresh(inventory_data)
    return inventory_data

def service_update_inventory(db: Session, inventory_update: InventoryUpdate) -> Inventory:
    """
    This function is used to update inventory.
    Args:
        db (Session): The database session.
        inventory_update (InventoryUpdate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory = db.exec(select(Inventory).where(Inventory.product_id == inventory_update.product_id)).first()
    if inventory is None:
        raise HTTPException(status_code=404,detail= "Not Found")
    inventory.quantity = inventory_update.quantity
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def service_reverse_inventory(db: Session, inventory_update: InventoryUpdate) -> Inventory:
    """
    This function is used to reverse inventory.
    Args:
        db (Session): The database session.
        inventory_update (InventoryUpdate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory = db.exec(select(Inventory).where(Inventory.product_id == inventory_update.product_id)).first()
    if inventory is None:
        raise HTTPException(status_code=404,detail= "Not Found")
    if inventory.quantity < inventory_update.quantity:
        raise HTTPException(status_code=400,detail= "Not enough quantity")
    inventory.quantity -= inventory_update.quantity
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def service_delete_inventory_by_id(db: Session, inventory: InventoryDelete):
    """
    This function is used to delete inventory.
    Args:
        db (Session): The database session.
        inventory (InventoryDelete): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory= db.exec(select(Inventory).where(Inventory.product_id == inventory.product_id)).first()
    db.delete(inventory)
    db.commit()
    return {"message":"inventory deleted"}
