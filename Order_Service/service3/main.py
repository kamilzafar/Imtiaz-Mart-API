from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session
from fastapi import FastAPI
from service3.service import *
from service3.db import create_db_and_tables, db_session
from typing import Annotated
from aiokafka import AIOKafkaProducer

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
    root_path="/order"
)

@app.get("/" ,tags=["Root"])
def get_root():
    return {"service":"Order Service"}

@app.get("/get", response_model = list[Order], tags=["Order"])
def get_order(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    order = service_get_order(db, user)
    return order

@app.get("/get/{order_id}", response_model = Order, tags=["Order"])
def get_order_by_id(order_id: int, db: Annotated[Session, Depends(db_session)],user: Annotated[User, Depends(get_current_user)]):
    order = service_get_order_by_id(db,order_id,user)
    return order

@app.post("/create",  response_model=Order, tags=["Order"])
async def create_order(order_data: OrderCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)], producer: Annotated[AIOKafkaProducer, Depends(produce_message)]) -> OrderRead:
    order = await service_create_order(session, order_data, user, producer)
    return order

@app.patch("/update", response_model = Order, tags=["Order"])
def update_order(order_update: OrderUpdate, order_id: int, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    order = service_get_order_by_id(session, order_id, user)
    if order is None:
        raise HTTPException(status_code=404,detail="Order not found!")
    order_data = order_update.model_dump(exclude_unset = True)
    order.sqlmodel_update(order_data)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order 

@app.delete("/delete", tags=["Order"])
def delete_order(order_id: int, user: Annotated[User, Depends(get_current_user)], session: Annotated[Session, Depends(db_session)]):
    deleted_order = service_delete_order(session, order_id, user)
    return deleted_order

@app.get("/cart", response_model = list[Cart], tags=["Cart"])
def get_cart(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    carts = db.exec(select(Cart).where(Cart.user_id == user.id)).all()
    if carts is None:
        raise HTTPException(status_code=200,detail="Cart is empty!")
    return carts

@app.get("/cart/product",  response_model = list[Product], tags=["Cart"])
def get_product_from_cart(cart_id: int, db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    return service_get_product_from_cart(db, user, cart_id)

@app.post("/cart/add",  response_model = Cart, tags=["Cart"])
def add_to_cart(cart_info: CartCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    cart = service_add_to_cart(session, cart_info, user)
    return cart

@app.patch("/cart/product/add", response_model = Cart, tags=["Cart"])
def update_cart_add(cart_id: int, cart_data: CartUpdate, db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    updated_cart = service_update_cart_add(db, cart_id, user, cart_data)
    return updated_cart

@app.patch("/cart/product/minus", response_model = Cart, tags=["Cart"])
def update_cart_minus(cart_id: int, product_id: int, db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    updated_cart = service_update_cart_minus(db, cart_id, user, product_id)
    return updated_cart

@app.delete("/cart/remove/{cart_id}", tags=["Cart"])
def remove_cart_by_id(cart_id: int, db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    service_remove_cart_by_id(db, user, cart_id)
    return {"message" : "Cart is removed"}

@app.get("/item", response_model = list[OrderItem], tags=["Orderitem"])
def get_order_item(order_id: int, db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]):
    orderitem = service_get_order_item(db, order_id, user)
    return orderitem

@app.get("/delivered", response_model = list[Order], tags=["Orderitem"])
def get_delivered_orders(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]):
    deivered_order = service_get_delivered_orders(db)
    return deivered_order

@app.get("/paid", response_model = list[Order], tags=["Orderitem"])
def get_delivered_orders(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]):
    paid_order = service_get_paid_orders(db)
    return paid_order

@app.get("/pending", response_model = list[Order], tags=["Orderitem"])
def get_pending_orders(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]):
    pending_order = service_get_pending_orders(db)
    return pending_order