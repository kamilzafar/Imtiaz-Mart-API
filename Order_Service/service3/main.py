from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from typing import Annotated, List
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI
from service3.setting import setting
from service3.service import *
from uuid import UUID, uuid4


connection_string = str(setting.DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

# Create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

def db_session():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="Product Service",
    description="Manages product catalog, including CRUD operations for products.",
    version="0.1",
    lifespan=lifespan,
    docs_url="/docs"
)

@app.get("/" ,tags=["Root"])
def get():
    pass

@app.get("/orders")
def get_order(db: Annotated[Session, Depends(db_session)]):
    pass

@app.post("/createorder")
def create_order(order_data:OrderCreate,session:Annotated[Session, Depends(db_session)],user = Depends(get_current_user)) -> OrderRead:
    
    order_info = Order.model_validate(order_data)
    order = service_create_order(session, order_info,user)
    return order

@app.patch("/updateorder")
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

@app.delete("/deleteorder")
def delete_order(order_id, user:Annotated[User, Depends(get_current_user)], session:Annotated[Session, Depends(get_session)]):
    deleted_order = service_delete_order(session,order_id)
    return deleted_order