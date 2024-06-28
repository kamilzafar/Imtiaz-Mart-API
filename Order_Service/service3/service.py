from jose import jwt, JWTError
from sqlmodel import Session,select
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from service3.models import *
from typing import Annotated
from service3 import setting
from service3.db import db_session

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def service_get_order(db:Session,user:User):
    """
    This function is used to get all orders.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: The list of orders.
    """
    orders = db.exec(select(Order).where(Order.user_id == user.id)).all()

    if orders is None:
        raise HTTPException(status_code=404, detail="order not found!")
    for order in orders:
        return order


def service_get_order_by_id(session:Session, order_id:int) -> Order:
    """
    This function is used to get a order by its id.
    Args:
        session (Session): The database session.
        order_id (int): The id of the order to retrieve.
    Returns:
        Order: The order object.
    """
    order = session.exec(select(Order).where(Order.order_id == order_id)).first()
    if order is None:
        raise HTTPException(status_code=404, detail="order not found!")
    return order


def service_create_order_item(session:Session,user:User,order_item_data:Cart,order_id:int):
    orderitem = OrderItem(order_id=order_id,product_id=order_item_data.product_id,product_size=order_item_data.product_size,product_total=order_item_data.product_total,user_id=user.id,total_cart_products=order_item_data.total_cart_products)
    session.add(orderitem)
    session.commit()
    session.refresh(orderitem)
    return orderitem


def service_delete_order_item(session:Session,order_id:int):
    orderitems = session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()
    for orderitem in orderitems:
        session.delete(orderitem)
    session.commit()
    return {"message":"Order item deleted!"}

def service_create_order(session:Session, order:Order, user:User) -> Order:
    """
    This function is used to create a new order.
    Args:
        session (Session): The database session.
        order (Order): The order data.
        user (User): The user object.
    Returns:
        Order: The order object.
    """
    existing_order = session.exec(select(Order).where(Order.order_id == order.order_id,Order.user_id == user.id)).first()
    if existing_order:
        raise HTTPException(status_code=404, detail="order is already present!")
    carts = session.exec(select(Cart).where(Cart.user_id == user.id)).all()
    if not carts:
        raise HTTPException(status_code=404,detail="Cart is Empty!")
    
    order.user_id = user.id
    session.add(order)
    session.commit()
    session.refresh(order)
    carts:Cart = service_get_cart_from_user(session,user)
    for cart in carts:
        if order:
            service_create_order_item(session,user,cart,order.order_id)
    
    for cart in carts:
        session.delete(cart)
        session.commit()  
    return order 


def service_delete_order(session:Session, order_id:int):
    """
    This function is used to delete an order by its id.
    Args:
        session (Session): The database session.
        order_id (int): The id of the order to delete.
    Returns:
        dict: The response message.
    """
    order = service_get_order_by_id(session, order_id)  
    session.delete(order)
    session.commit()
    return {"message":"order deleted"}

def service_order_update(session:Session,user:User,order_id:int):
    """
    This function is used to update an order.
    Args:
        session (Session): The database session.
        order_id (int): The id of the order to update.
    Returns:
        simplejson: The response message.
    """
    order = service_get_order_by_id(session,order_id)
    if order.order_status == "cancelled":
        service_delete_order_item(session,order_id)
        service_delete_order(session,order_id)
        return {"message":"Order is cancelled"}
    elif order.order_status == "delivered":
        service_delete_order_item(session,order_id)
        service_delete_order(session,order_id)
        return {"message":"Order is delivered"}
    
def service_get_cart_from_user(session:Session,user:User):
    carts = session.exec(select(Cart).where(Cart.user_id == user.id)).all()
    return carts

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


def service_add_same_product_to_cart(session:Session,user:User,cart_updated_data:Cart):
    cart_row = session.exec(select(Cart).where(Cart.user_id == user.id,Cart.product_id == cart_updated_data.product_id,Cart.product_size == cart_updated_data.product_size)).first()
    product:Product = session.exec(select(Product).where(Product.product_id == cart_updated_data.product_id)).first() 
    if cart_row:
        cart_row.total_cart_products += cart_updated_data.total_cart_products 
        cart_row.product_total = cart_row.total_cart_products * product.product_price
        session.add(cart_row)
        session.commit()
        return cart_row

def service_add_to_cart(session:Session,cart_data:Cart,user:User,product_id:int):
    
    if not user:
        raise HTTPException(status_code=401,detail="User not found!")
    
    cart_data.user_id = user.id
    cart_data.product_id = product_id
    cart = session.exec(select(Cart).where(Cart.user_id == user.id,Cart.product_id == product_id, Cart.product_size == cart_data.product_size)).first()
    if cart:
        return service_add_same_product_to_cart(session,user,cart_data)
    session.add(cart_data)
    session.commit()
    session.refresh(cart_data)


    return cart_data


def service_remove_cart_by_id(db:Session,user:User,cart_id:int):
    cart = db.exec(select(Cart).where(Cart.cart_id == cart_id,Cart.user_id == user.id)).first()
    if cart is None:
        raise HTTPException(status_code=404,detail="Cart not found!")
    db.delete(cart)
    db.commit()

def service_remove_cart(db:Session,user:User):
    carts = db.exec(select(Cart).where(Cart.user_id == user.id)).all()
    for cart in carts:
        db.delete(cart)
    db.commit()
     


def service_get_product_from_cart(session:Session,user:User):
    product_from_cart = session.exec(select(Product).join(Cart).where(Cart.user_id == user.user_id))
    return product_from_cart