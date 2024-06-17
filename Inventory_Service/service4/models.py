from sqlmodel import SQLModel,Field,Column
from enum import Enum

class InventoryBase(SQLModel):
    quantity:int 


class Inventory(InventoryBase):
    inventory_id:int | None = Field(primary_key=True,default=None)
    product_id:int | None = Field(foreign_key="product.id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None) 
    user_id:int | None = Field(foreign_key="user.id",default=None)

class InventoryCreate(Inventory):
    pass

class InventoryRead(Inventory):
    pass

class Size(str,Enum):
    LARGE:str = "large"
    SMALL:str = "small"
    MEDIUM:str = "medium"

class OrderStatus(str,Enum):
    PENDING:str = "pending"
    CANCELLED:str = "cancelled"
    DELIVERED:str = "delivered"

class OrderBase(SQLModel):
    order_status:OrderStatus
    customer_name:str
    customer_email:str


class Order(OrderBase,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.id",default=None)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(SQLModel):
    order_status:OrderStatus

class OrderRead(OrderBase):
    pass

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    
class User(UserBase, table=True):
    id: int | None = Field(primary_key=True, index=True,default=None)

class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    filename: str
    content_type: str
    image_data: bytes

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    furniture = "furniture"
    
class ProductBase(SQLModel):
    name: str
    description: str
    price: int
    stock: int
    category: Category = Field(default=Category.clothing,sa_column=Column("category", Enum(Category)))
    image_id: int = Field(foreign_key="image.id")

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass