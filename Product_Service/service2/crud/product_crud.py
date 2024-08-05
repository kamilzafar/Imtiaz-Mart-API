from fastapi import HTTPException
from sqlmodel import Session, select
from service2.models import Product, ProductCreate, User

def create_product(session: Session, product: ProductCreate, user: User) -> Product:
    """
    Create a new product.
    Args:
        session (Session): The database session.
        product (ProductCreate): The product object.
        user (User): The user object.
    Returns:
        Product: The created product object.
    """
    product = Product(**product.model_dump(), user_id=user.id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


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

def delete_product(session: Session, product_id: int) -> dict:
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
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully."}