from fastapi import FastAPI, Request, Depends
from fastapi.security import OAuth2PasswordBearer
# from service6.db import create_db_and_tables
from contextlib import asynccontextmanager
from service6.model import Order, User
from service6.service import generate_checkout_session, service_get_order, get_current_user
from service6 import settings
import json
import stripe
from typing import Annotated

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    # create_db_and_tables()
    yield

app = FastAPI(
    title="Payment Service",
    description="Processes payments and manages transaction records.",
    version="0.1",
    root_path="/payment",
    lifespan=lifespan
)

stripe.api_key = settings.SECRET_KEY_STRIPE

@app.get("/", tags=["Root"])
def get_root():
  return {"service": "Payment Service"}



@app.post("/payment")
def process_payment(order_id: int, user: Annotated[User, Depends(get_current_user)]):
  order: Order = service_get_order(order_id, user)
  payment = generate_checkout_session(order)
  return payment


# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = settings.WB_SECRET_KEY


@app.post('/webhook')
def webhook(request:Request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
    if event['type'] == 'checkout.session.async_payment_failed':
      session = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
      session = event['data']['object']
    elif event['type'] == 'checkout.session.completed':
      session = event['data']['object']
    elif event['type'] == 'checkout.session.expired':
      session = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return json.load(success=True)