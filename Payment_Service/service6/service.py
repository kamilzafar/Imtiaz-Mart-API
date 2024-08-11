import stripe
from typing import Any
import requests
from fastapi import HTTPException
from service6 import settings
from service6.model import *

def generate_checkout_session():
    

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

def service_get_order(order_id:int) -> Order:
    Order = requests.get(f"{settings.ORDER_SERVICE_URL}/get/{order_id}")
    if Order.status_code != 200:
        raise HTTPException(status_code=404, detail="Order not found")
    order = Order(**Order.json())
    return order

def service_get_order_item(order_id:int) -> list[OrderItem]:
    Orderitem = requests.get(f"{settings.ORDER_SERVICE_URL}/item? order_id = {order_id}")
    if Orderitem.status_code != 200:
        raise HTTPException(status_code=404, detail="Order Item not found!")
    orderitem = OrderItem(**Orderitem.json())
    return orderitem

def service_get_product(product_id:int) -> Product:
    response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/product/{product_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found!")
    product = Product(**response.json())
    return product