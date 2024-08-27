from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import stripe
import requests
from fastapi import Depends, HTTPException, status
from service6 import settings
from service6.model import Order, Product, User

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
    response = requests.get(f"{settings.USER_SERVICE_URL}/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    user = User(**response.json())
    if user is None:
        raise credentials_exception
    return user

def generate_checkout_session(order: Order):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'pkr',                    
                    'product_data': {
                        'name': '',
                        'description': '',
                        'price':"",
                        'category':""
                    },
                    'unit_amount': order.total_price * 100,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url="",
        cancel_url="",
    )
    return checkout_session

def service_get_order(order_id: int, user: Annotated[User, Depends(get_current_user)]) -> Order:
    order = requests.get(f"{settings.ORDER_SERVICE_URL}/get/{order_id}")
    if order.status_code != 200:
        raise HTTPException(status_code=404, detail="Order not found")
    order = Order(**order.json())
    return order

# def service_get_order_item(order_id:int) -> list[OrderItem]:
#     Orderitem = requests.get(f"{settings.ORDER_SERVICE_URL}/item? order_id = {order_id}")
#     if Orderitem.status_code != 200:
#         raise HTTPException(status_code=404, detail="Order Item not found!")
#     orderitem = OrderItem(**Orderitem.json())
#     return orderitem

def service_get_product(product_id: int) -> Product:
    response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/product/{product_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found!")
    product = Product(**response.json())
    return product