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

@app.get("/", tags=["Root"])
def main():
    return {"service" : "Inventory service"}

@app.get("/check/{product_id}", tags=["Inventory"])
def get_inventory(product_id: int, db: Annotated[Session, Depends(db_session)]):
    invetory = service_get_inventory(db, product_id)
    return invetory

@app.post("/create", response_model=Inventory, tags=["Inventory"])
def create_inventory(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)], inventory_data: InventoryCreate):
    inventory_info= Inventory.model_validate(inventory_data)
    inventory = service_create_inventory(db, inventory_info)
    return inventory

@app.patch("/update", response_model = Inventory, tags=["Inventory"])
def update_inventory(db: Annotated[Session, Depends(db_session)], inventory_data: InventoryUpdate):
    return service_update_inventory(db, inventory_data)

@app.delete("/product", tags=["Inventory"])
def remove_product_quantity(db: Annotated[Session, Depends(db_session)], inventory: InventoryUpdate):
    return service_reverse_inventory(db, inventory)

@app.delete("/delete", tags=["Inventory"])
def delete_inventory_by_id(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)], inventory: InventoryDelete):
    return service_delete_inventory_by_id(db, inventory)