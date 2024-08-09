from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from service6.db import create_db_and_tables
from contextlib import asynccontextmanager
from service6.service import *

app = FastAPI(
    title="Payment Service",
    description="Processes payments and manages transaction records.",
    version="0.1",
    root_path="/payment"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.get("/", tags=["Root"])
def get_root():
    return {"service": "Payment Service"}



@app.post("/payment")
def process_payment(order_id:int):
    payment = generate_checkout_session(order_id)
    return payment

