from sqlmodel import SQLModel, Field

class InventoryBase(SQLModel):
    product_id: int
    quantity: int 

class Inventory(InventoryBase):
    inventory_id: int = Field(primary_key=True,default=None)
    inventory_name: str

class InventoryCreate(InventoryBase): 
    pass

class InventoryUpdate(SQLModel): 
   pass