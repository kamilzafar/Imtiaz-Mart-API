from sqlmodel import Session,select
from fastapi import HTTPException
from models import *

def service_get_order(db:Session):
    order = db.exec(select(Order)).all()
    if order is None:
        raise HTTPException(status_code=404, detail="order not found!")
    return order


def service_get_order_by_id(session:Session, order_id:int) -> Order:
    """

    """
    order = session.exec(select(Order).where(Order.order_id == order_id)).first()
    if order is None:
        raise HTTPException(status_code=404, detail="order not found!")
    return order


def service_create_order_item(session:Session,user:User,order_item_data:Cart,order_id:int):
    orderitem = OrderItem(order_id=order_id,product_id=order_item_data.product_id,product_size=order_item_data.product_size,product_total=order_item_data.product_total,user_id=user.user_id,total_cart_products=order_item_data.total_cart_products)
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

    """
    existing_order = session.exec(select(Order).where(Order.order_id == order.order_id,Order.user_id == user.user_id)).first()
    if existing_order:
        raise HTTPException(status_code=404, detail="order is already present!")
    carts = session.exec(select(Cart).where(Cart.user_id == user.user_id)).all()
    if not carts:
        raise HTTPException(status_code=404,detail="Cart is Empty!")
    
    order.user_id = user.user_id
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
    order = service_get_order_by_id(session, order_id)  
    session.delete(order)
    session.commit()
    return {"message":"order deleted"}

def service_order_update(session:Session,user:User,order_id:int):
    order = service_get_order_by_id(session,order_id)
    if order.order_status == "cancelled":
        service_delete_order_item(session,order_id)
        service_delete_order(session,order_id)
        return {"message":"Order is cancelled"}
    elif order.order_status == "delivered":
        service_delete_order_item(session,order_id)
        service_delete_order(session,order_id)
        return {"message":"Order is delivered"}