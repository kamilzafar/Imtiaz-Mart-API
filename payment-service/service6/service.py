import stripe
from typing import Any
import requests
from fastapi import HTTPException
from service6 import settings

def generate_checkout_session(order_id:int):
    order = service_get_order(order_id) 
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'pkr',
                    'product_data': {
                        'name': 'Quarter 1 Voucher',
                        'description': 'Voucher for Quarter 1',
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

def service_get_order(order_id:int):
    Order = requests.get(f"{settings.ORDER_SERVICE_URL}/get/{order_id}")
    if Order.status_code != 200:
        raise HTTPException(status_code=404, detail="Inventory not found!")
    order = Order(**Order.json())
    return order