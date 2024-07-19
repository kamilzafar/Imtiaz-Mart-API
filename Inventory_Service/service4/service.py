from sqlmodel import Session,select
from service4.models import *
from service4.database import *
from fastapi import HTTPException,Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from service4 import setting
from jose import jwt, JWTError


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# user

def get_current_user(token:Annotated[str,Depends(oauth_scheme)],session:Session = Depends(db_session)) -> User:
    """
    This function is used to get the current user from the token.
    Args:
        token (str): The access token.
        db (Session): The database session.
    Returns:
        User: The user object.
    """
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})                 
    try:
        payload = jwt.decode(token, setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    user = get_user_by_username(session,token_data.username)
    if user is None:
        raise credentials_exception
    return user



def get_user_by_username(session:Session,username:str) -> User:
    """
    This function is used to get a user by its username.
    Args:
        session (Session): The database session.
        username (str): The username of the user to retrieve.
    Returns:
        User: The user object.
    """
    if not username:
        return None
    
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found!")
    return user 


# Inventory

def service_get_inventory(db:Session,user:User):
    inventories = db.exec(select(Inventory).where(Inventory.user_id == user.id)).all()
    for inventory in inventories:
        return inventory
    
def service_get_product_from_inventory(db:Session,user:User,inventory_id:int):
    inventory= db.exec(select(Inventory).where(Inventory.user_id== user.id,Inventory.inventory_id == inventory_id)).first()
    product = db.exec(select(Product).where(inventory.product_id == Product.id))
    return product
    
def service_create_inventory(db:Session,inventory_data:Inventory,user:User):
    inventory_data.user_id = user.id
    db.add(inventory_data)
    db.commit()
    db.refresh(inventory_data)
    return inventory_data

def service_update_inventory(db:Session,user:User,inventory_update:Inventory,inventory_id:int):
    inventory = db.exec(select(Inventory).where(Inventory.inventory_id == inventory_id)).first()
    if inventory is None:
        raise HTTPException(status_code=404,detail= "Not Found")
    inventory.quantity = inventory_update.quantity
    db.commit()
    return {"message":"quantity updated"}

def service_delete_inventory(db:Session,user:User):
    inventories = db.exec(select(Inventory).where(Inventory.user_id== user.id)).all()
    for inventory in inventories:
        db.delete(inventory)
    db.commit()
    return {"message":"inventories deleted"}

def service_delete_inventory_by_id(db:Session,user:User,inventory_id:int):
    inventory= db.exec(select(Inventory).where(Inventory.user_id== user.id,Inventory.inventory_id == inventory_id)).first()
    db.delete(inventory)
    db.commit()
    return {"message":"inventory deleted"}
