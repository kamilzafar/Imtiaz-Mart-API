from sqlmodel import Session,select
from service4.models import *
from fastapi import HTTPException

def service_get_inventory(db:Session):
    inventories = db.exec(select(Inventory)).all()
    for inventory in inventories:
        return inventory
    
def service_create_inventory(db:Session,inventory_data:InventoryCreate):
    existing_inventory = db.exec(select(Inventory).where(Inventory.inventory_id == inventory_data.inventory_id)).first()
    if existing_inventory:
        raise HTTPException(status_code=400,detail="Inventory already exist")
    inventory = Inventory.model_validate(inventory_data)
    db.add(inventory)
    db.commit()
    return inventory