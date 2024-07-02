from fastapi import FastAPI
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session
from fastapi import FastAPI
from service4.models import *
from service4.service import *
from service4.database import *

app = FastAPI(
    title="Inventory Service",
    description="Manages stock levels and inventory updates",
    version="0.1",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/inventory"
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