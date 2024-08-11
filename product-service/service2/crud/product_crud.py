from fastapi import HTTPException
import requests
from sqlmodel import Session, select
from service2.models.inventory_models import Inventory, InventoryCreate, InventoryUpdate
from service2.models.product_models import Product, ProductCreate, ProductUpdate
from service2.models.user_models import User
from service2.settings import INVENTORY_SERVICE_URL

def create_product_inventory(inventory: InventoryCreate, token: str) -> Inventory:
    """
    Create a new inventory.
    Args:
        inventory (InventoryCreate): The inventory object.
    Returns:
        Inventory: The created inventory object.
    """
    request = requests.post(
        f"{INVENTORY_SERVICE_URL}/inventory/create", 
        json=inventory.dict(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    if request.status_code != 200:
        raise HTTPException(status_code=request.status_code, detail=request.json())
    return Inventory(**request.json())

def create_new_product(session: Session, product: ProductCreate, user: User, token: str) -> Product:
    """
    Create a new product.
    Args:
        session (Session): The database session.
        product (ProductCreate): The product object.
        user (User): The user object.
    Returns:
        Product: The created product object.
    """
    new_product = Product(**product.model_dump(), user_id=user.id)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    inventory = InventoryCreate(
        inventory_name=product.name,
        product_id=new_product.id,
        quantity=product.quantity,
    )
    create_product_inventory(inventory, token)
    
    return new_product

def get_all_products(session: Session) -> list[Product]:
    """
    Get all products.
    Args:
        session (Session): The database session.
    Returns:
        List[Product]: The list of products.
    """
    products = session.exec(select(Product)).all()
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def get_product_by_id(session: Session, product_id: int) -> Product:
    """
    Get a product by its ID.
    Args:
        session (Session): The database session.
        product_id (int): The product ID.
    Returns:
        Product: The product object.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_product_by_name(session: Session, product_name: str) -> list[Product]:
    """
    Get a product by its name.
    Args:
        session (Session): The database session.
        product_name (str): The product name.
    Returns:
        List[Product]: The list of products.
    """
    products = session.exec(select(Product).where(Product.name.contains(product_name))).all()
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products

def update_product_inventory(inventory: InventoryUpdate, token: str) -> Inventory:
    """
    Update an inventory.
    Args:
        inventory (InventoryCreate): The inventory object.
    Returns:
        Inventory: The updated inventory object.
    """
    request = requests.patch(
        f"{INVENTORY_SERVICE_URL}/inventory/update", 
        json=inventory.dict(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    if request.status_code != 200:
        raise HTTPException(status_code=request.status_code, detail=request.json())
    return Inventory(**request.json())

def update_product_in_db(session: Session, product_id: int, product: ProductUpdate, token: str) -> Product:
    """
    Update a product by its ID.
    Args:
        session (Session): The database session.
        product_id (int): The product ID.
        product (ProductCreate): The product object.
    Returns:
        Product: The updated product object.
    """
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_inventory = InventoryUpdate(product_id=product_id, quantity=product.quantity)
    update_product_inventory(updated_inventory, token)
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product_db, key, value)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db

def delete_product_inventory(product_id: int, token: str) -> dict:
    """
    Delete an inventory by its product ID.
    Args:
        product_id (int): The product ID.
    Returns:
        Dict: The response message.
    """
    request = requests.delete(
        f"{INVENTORY_SERVICE_URL}/inventory/delete", 
        json={"product_id": product_id},
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
    if request.status_code != 200:
        raise HTTPException(status_code=request.status_code, detail=request.json())
    return {"message": "Inventory deleted successfully."}

def delete_product_from_db(session: Session, product_id: int, token: str) -> dict:
    """
    Delete a product by its ID.
    Args:
        session (Session): The database session.
        product_id (int): The product ID.
    Returns:
        Dict: The response message.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_product_inventory(product_id, token)
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully."}