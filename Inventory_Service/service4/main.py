from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session
from fastapi import FastAPI
from service4.models import *
from service4.service import *
from service4.database import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

app = FastAPI(
    title="Inventory Service",
    description="Manages stock levels and inventory updates",
    version="0.1",
    lifespan=lifespan,
    root_path="/inventory"
)

@app.get("/")
def main():
    return {"service":"Inventory service"}


@app.get("/get-inventory")
def get_inventory(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)]):
    invetory = service_get_inventory(db,user)
    return invetory

@app.get("/getproduct",response_model=Product)
def get_product_by_inventory(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)],inventory_id:int):
    return service_get_product_from_inventory(db,user,inventory_id)

@app.post("/create-inventory",response_model=InventoryRead)
def create_inventory(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)],inventory_data:InventoryCreate):
    inventory_info= Inventory.model_validate(inventory_data)
    inventory = service_create_inventory(db,inventory_info,user)
    return inventory

@app.patch("/update-inventory")
def update_inventory(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)],inventory_data:InventoryUpdate,inventory_id:int):
    return service_update_inventory(db,user,inventory_data,inventory_id)

@app.delete("/delete-inventory")
def delete_inventory(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)]):
    return service_delete_inventory(db,user)

@app.delete("/delete-inventory/{inventory_id}")
def delete_inventory_by_id(db:Annotated[Session,Depends(db_session)],user:Annotated[User,Depends(get_current_user)],inventory_id:int):
    return service_delete_inventory_by_id(db,user,inventory_id)