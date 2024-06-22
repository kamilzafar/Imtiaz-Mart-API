from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session
from fastapi import FastAPI
from service3.service import *
from service3.db import create_db_and_tables, db_session
from typing import Annotated

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

app = FastAPI(
    title="Order Service",
    description="Handles order creation, updating, and tracking",
    version="0.1",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/order"
)

@app.get("/" ,tags=["Root"])
def get_root():
    return {"service":"Order Service"}

@app.get("/orders", tags=["Order"])
def get_order(db: Annotated[Session, Depends(db_session)]):
    pass

@app.post("/createorder", response_model=Order, tags=["Order"])
def create_order(order_data:OrderCreate,session:Annotated[Session, Depends(db_session)],user = Depends(get_current_user)) -> OrderRead:
    
    order_info = Order.model_validate(order_data)
    order = service_create_order(session, order_info,user)
    return order

@app.patch("/updateorder", response_model=Order, tags=["Order"])
def update_order(order_update:OrderUpdate,order_id,session:Annotated[Session, Depends(db_session)], user = Depends(get_current_user)):
    order = service_get_order_by_id(session,order_id)
    if order:
        order_data = order_update.model_dump(exclude_unset = True)
        order.sqlmodel_update(order_data)
        session.add(order)
        session.commit()
        session.refresh(order)
        if order.order_status == "cancelled" or order.order_status == "delivered":
            return service_order_update(session,user,order_id)
        return order 

@app.delete("/deleteorder", tags=["Order"])
def delete_order(order_id, user:Annotated[User, Depends(get_current_user)], session:Annotated[Session, Depends(db_session)]):
    deleted_order = service_delete_order(session,order_id)
    return deleted_order

