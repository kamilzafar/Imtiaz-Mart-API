from jose import jwt, JWTError
import requests
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from service3.models import *
from typing import Annotated, List
from service3 import setting
import service3.order_pb2 as order_pb2
from aiokafka import AIOKafkaProducer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def produce_message():
    producer = AIOKafkaProducer(bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVER)
    await producer.start()
    try:
        # Produce message
        yield producer
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

def get_product(product_id: int):
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

def service_get_order(db:Session, user:User):
    """
    This function is used to get all orders.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: The list of orders by user.
    """
    orders = db.exec(select(Order).where(Order.user_id == user.id)).all()
    if orders is None:
        raise HTTPException(status_code=200, detail="No orders found!")
    return orders

def service_get_order_by_id(session: Session, order_id: int, user: User) -> Order:
    """
    This function is used to get a order by its id.
    Args:
        session (Session): The database session.
        order_id (int): The id of the order to retrieve.
    Returns:
        Order: The order object.
    """
    order = session.exec(select(Order).where(Order.order_id == order_id, Order.user_id == user.id)).first()
    if order is None:
        raise HTTPException(status_code=404, detail="order not found!")
    return order


def service_create_order_item(session: Session, user: User, order_item_data: Cart, order_id: int):
    orderitem = OrderItem(
        order_id=order_id,
        product_id=order_item_data.product_id, 
        price=order_item_data.product_total,
        user_id=user.id,
        quantity=order_item_data.quantity
    )
    session.add(orderitem)
    session.commit()
    session.refresh(orderitem)
    return orderitem


def service_delete_order_item(session: Session, order_id: int):
    orderitems = session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()
    for orderitem in orderitems:
        session.delete(orderitem)
    session.commit()
    return {"message":"Order item deleted!"}

async def service_create_order(session: Session, order_data: Order, user: User, producer: Annotated[AIOKafkaProducer, Depends(produce_message)]) -> Order:
    """
    This function is used to create a new order.
    Args:
        session (Session): The database session.
        order (Order): The order data.
        user (User): The user object.
    Returns:
        Order: The order object.
    """
    carts = session.exec(select(Cart).where(Cart.user_id == user.id)).all()
    if not carts:
        raise HTTPException(status_code=404,detail="Cart is Empty!")
    order_data.user_id = user.id
    Kafka_order = order_pb2.Order(order_id = order_data.order_id, username= order_data.customer_name, useremail = order_data.customer_email)
    serialized_order = Kafka_order.SerializeToString()
    await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC,serialized_order)
    session.add(order_data)
    session.commit()
    session.refresh(order_data)
    carts:Cart = service_get_cart_from_user(session,user)
    for cart in carts:
        service_create_order_item(session, user, cart, order_data.order_id)
        session.delete(cart)
        session.commit()  
    return order_data 


def service_delete_order(session: Session, order_id: int, user: User):
    """
    This function is used to delete an order by its id.
    Args:
        session (Session): The database session.
        order_id (int): The id of the order to delete.
    Returns:
        dict: The response message.
    """
    order = service_get_order_by_id(session, order_id,user)  
    session.delete(order)
    session.commit()
    return {"message":"order deleted"}

def service_get_order_item(db: Session, order_id: int, user: User) -> List[OrderItem]:
    """
    This function is used to get order items by order id.
    Args:
        db (Session): The database session.
        order_id (int): The id of the order.
    Returns:
        List[OrderItem]: The list of order items.
    """
    order = service_get_order_by_id(db, order_id, user)
    order_items = db.exec(select(OrderItem).where(OrderItem.order_id == order.order_id)).all()
    return order_items
    
def service_get_cart_from_user(session: Session, user: User) -> List[Cart]:
    """
    This function is used to get all carts by user.
    Args:
        session (Session): The database session.
        user (User): The user object.
    Returns:
        List[Cart]: The list of carts
    """
    carts = session.exec(select(Cart).where(Cart.user_id == user.id)).all()
    return carts

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
    response = requests.get(f"{setting.USER_SERVICE_URL}/auth/users/me", headers={"Authorization": f"Bearer {token}"})
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

def service_add_same_product_to_cart(session: Session, user: User, cart_updated_data: Cart) -> Cart:
    """
    This function is used to add the same product to the cart.
    Args:
        session (Session): The database session.
        user (User): The user object.
        cart_updated_data (Cart): The cart data.
    Returns:
        Cart: The cart object.
    """
    cart_row = session.exec(select(Cart).where(Cart.user_id == user.id,Cart.product_id == cart_updated_data.product_id)).first()
    product: Product = get_product(cart_updated_data.product_id) 
    inventory = session.exec(select(Inventory).where(Inventory.product_id == product.id)).first()
    if cart_row.quantity > inventory.quantity:
        raise HTTPException(status_code=200, detail="We are out of stock!")
    if cart_row:
        cart_row.quantity += cart_updated_data.quantity 
        cart_row.product_total = cart_row.quantity * product.price
        session.add(cart_row)
        session.commit()
        return cart_row

def service_add_to_cart(session: Session, cart_data: CartCreate, user: User) -> Cart:
    """
    This function is used to add a product to the cart.
    Args:
        session (Session): The database session.
        cart_data (CartCreate): The cart data.
        user (User): The user object.
    Returns:
        Cart: The cart object.
    """
    inventory = session.exec(select(Inventory).where(Inventory.product_id == cart_data.product_id)).first()
    if cart_data.quantity > inventory.quantity:
        raise HTTPException(status_code=200,detail="We are out of stock!")
    product: Product = get_product(cart_data.product_id)
    product_total = cart_data.quantity * product.price
    user_cart = Cart(user_id=user.id, product_id=cart_data.product_id, quantity=cart_data.quantity, product_total= product_total)
    cart = session.exec(select(Cart).where(Cart.user_id == user.id,Cart.product_id == cart_data.product_id)).first()
    if cart:
        return service_add_same_product_to_cart(session, user, user_cart)
    session.add(user_cart)
    session.commit()
    session.refresh(user_cart)
    return user_cart

def service_remove_cart_by_id(db: Session, user: User, cart_id: int) -> Cart:
    """
    This function is used to remove a cart by its id.
    Args:
        db (Session): The database session.
        user (User): The user object.
        cart_id (int): The id of the cart to remove.
    Returns:
        Cart: The cart object.
    """
    cart = db.exec(select(Cart).where(Cart.cart_id == cart_id, Cart.user_id == user.id)).first()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found!")
    db.delete(cart)
    db.commit()
    db.refresh(cart)
    return cart

def service_remove_cart(db: Session, user: User):
    """
    This function is used to remove all carts.
    Args:
        db (Session): The database session.
        user (User): The user object.
    """
    carts = db.exec(select(Cart).where(Cart.user_id == user.id)).all()
    for cart in carts:
        db.delete(cart)
    db.commit()
    db.refresh(cart)
    return {"message":"All carts are removed!"}
     
def service_update_cart_add(db: Session, cart_id: int, user: User, product_id: int) -> Cart:
    """
    This function is used to update the quantity of a product in the cart.
    Args:
        db (Session): The database session.
        cart_id (int): The id of the cart.
        user (User): The user object.
        product_id (int): The id of the product.
    Returns:
        Cart: The cart object.
    """
    cart = db.exec(select(Cart).where(Cart.cart_id == cart_id, Cart.user_id == user.id)).first()
    product: Product = get_product(product_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found!")
    cart.quantity +=1
    cart.product_total = cart.quantity * product.price
    return cart

def service_update_cart_minus(db: Session, cart_id: int, user: User, product_id: int) -> Cart:
    """
    This function is used to update the quantity of a product in the cart.
    Args:
        db (Session): The database session.
        cart_id (int): The id of the cart.
        user (User): The user object.
        product_id (int): The id of the product.
    Returns:
        Cart: The cart object.
    """
    cart = db.exec(select(Cart).where(Cart.cart_id == cart_id,Cart.user_id == user.id)).first()
    product: Product = get_product(product_id) 
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found!")
    cart.quantity -=1
    cart.product_total = cart.quantity * product.price
    return cart

def service_get_cart_by_id(db: Session, cart_id: int, user: User) -> Cart:
    """
    This function is used to get a cart by its id.
    Args:
        db (Session): The database session.
        cart_id (int): The id of the cart to retrieve.
    Returns:
        Cart: The cart object.
    """
    cart = db.exec(select(Cart).where(Cart.cart_id == cart_id,Cart.user_id == user.id)).first()
    return cart

def service_get_product_from_cart(db: Session, user: User, cart_id: int) -> List[Product]:
    """
    This function is used to get products from cart.
    Args:
        db (Session): The database session.
        user (User): The user object.
        cart_id (int): The id of the cart.
    Returns:
        List[Product]: The list of products in the cart.
    """
    carts = db.exec(select(Cart).where(Cart.cart_id == cart_id, Cart.user_id == user.id)).all()
    if carts is None:
        raise HTTPException(status_code=200, detail="Cart is empty!")
    products: List[Product] = []
    for cart in carts:
        product: Product = get_product(cart.product_id)
        products.append(product)
    return products

def service_get_paid_orders(db: Session) -> List[Order]:
    """
    This function is used to get all paid orders by admin.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: The list of paid orders.
    """
    paid_order = db.exec(select(Order).where(Order.order_status == "paid")).all()
    return paid_order

def service_get_pending_orders(db: Session) -> List[Order]:
    """
    This function is used to get all pending orders by admin.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: The list of pending orders.
    """
    pending_order = db.exec(select(Order).where(Order.order_status == "pending")).all()
    return pending_order

def service_get_delivered_orders(db: Session) -> List[Order]:
    """
    This function is used to get all delivered orders by admin.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: The list of delivered orders.
    """
    delivered_order = db.exec(select(Order).where(Order.order_status == "delivered")).all()
    return delivered_order