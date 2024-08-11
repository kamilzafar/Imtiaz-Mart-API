from sqlmodel import SQLModel, Field
from uuid import UUID

class CartBase(SQLModel):
    product_id: int
    quantity: int

class Cart(CartBase, table = True): 
    cart_id: int = Field(primary_key=True,default=None)
    user_id: UUID 
    product_total: int

class CartCreate(CartBase): 
    pass    

class CartUpdate(CartBase):
    pass

class CartRead(CartBase):
    cart_id: int
    user_id: UUID
    product_id: int
