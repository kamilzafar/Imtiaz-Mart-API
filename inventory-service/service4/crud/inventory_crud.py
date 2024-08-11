from sqlmodel import Session, select
from fastapi import HTTPException
from service4.service import get_product
from service4.models.inventory_model import Inventory, InventoryCreate, InventoryUpdate, InventoryDelete

def service_get_inventory(db: Session, product_id: int) -> Inventory:
    """
    This function is used to get inventory by product id.
    Args:
        db (Session): The database session.
        product_id (int): The id of the product.
    Returns:
        dict: The inventory object.
    """
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    inventory = db.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory Not Found")
    return inventory
    
def service_create_inventory(db: Session, inventory_data: InventoryCreate) -> Inventory:
    """
    This function is used to create inventory.
    Args:
        db (Session): The database session.
        inventory_data (InventoryCreate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory_data = Inventory(
        inventory_name=inventory_data.inventory_name,
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity,
    )
    db.add(inventory_data)
    db.commit()
    db.refresh(inventory_data)
    return inventory_data

def service_update_inventory(db: Session, inventory_update: InventoryUpdate) -> Inventory:
    """
    This function is used to update inventory.
    Args:
        db (Session): The database session.
        inventory_update (InventoryUpdate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory = db.exec(select(Inventory).where(Inventory.product_id == inventory_update.product_id)).first()
    if inventory is None:
        raise HTTPException(status_code=404,detail= "Not Found")
    inventory.quantity = inventory_update.quantity
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def service_reverse_inventory(db: Session, inventory_update: InventoryUpdate) -> Inventory:
    """
    This function is used to reverse inventory.
    Args:
        db (Session): The database session.
        inventory_update (InventoryUpdate): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory = db.exec(select(Inventory).where(Inventory.product_id == inventory_update.product_id)).first()
    if inventory is None:
        raise HTTPException(status_code=404,detail= "Not Found")
    if inventory.quantity < inventory_update.quantity:
        raise HTTPException(status_code=400,detail= "Not enough quantity")
    inventory.quantity -= inventory_update.quantity
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def service_delete_inventory_by_id(db: Session, inventory: InventoryDelete):
    """
    This function is used to delete inventory.
    Args:
        db (Session): The database session.
        inventory (InventoryDelete): The inventory data.
    Returns:
        dict: The inventory object.
    """
    inventory= db.exec(select(Inventory).where(Inventory.product_id == inventory.product_id)).first()
    db.delete(inventory)
    db.commit()
    return {"message":"inventory deleted"}