from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI
from service4.models import *
from service4.setting import DATABASE_URL
from service4.service import *

connection_string = str(DATABASE_URL)

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
    title="Inventory Service",
    description="Manages stock levels and inventory updates",
    version="0.1",
    lifespan=lifespan,
    docs_url="/docs"
)

@app.get("/")
def main():
    return {"message":"Inventory service"}


@app.get("/inventory")
def get_inventory(db:Annotated[Session,Depends(db_session)]):
    invetory = service_get_inventory(db)
    return invetory

@app.post("/create-inventory")
def create_inventory(db:Annotated[Session,Depends(db_session)],inventory_data:InventoryCreate):
    inventory = service_create_inventory(db,inventory_data)
    return inventory