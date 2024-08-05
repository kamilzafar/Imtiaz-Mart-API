from fastapi import FastAPI, Depends
from typing import Annotated, List
from service2.services import check_admin
from service2.models.user_models import User
from service2.models.product_models import Product, ProductCreate
from service2.crud.product_crud import create_product, get_all_products, get_product_by_id, get_product_by_name, delete_product
from sqlmodel import Session
from service2.databse.db import db_session, lifespan

app = FastAPI(
    title="Product Service",
    description="Manages product catalog, including CRUD operations for products.",
    version="0.1",
    lifespan=lifespan,
    root_path="/product",
)

@app.get("/", tags=["Root"])
def read_root():
    return {"service": "Product Service"}

@app.post("/create", response_model=Product, tags=["Product"])
def create_product(product: ProductCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]):
    new_product = create_product(session, product, user)
    return new_product

@app.get("/all-products", response_model=List[Product], tags=["Product"])
def read_products(session: Annotated[Session, Depends(db_session)]):
    products = get_all_products(session)
    return products

@app.get("/search", response_model=List[Product], tags=["Product"])
def get_product_by_name(product_name: str, session: Annotated[Session, Depends(db_session)]):
    product = get_product_by_name(session, product_name)
    return product

@app.get("/{product_id}", response_model=Product, tags=["Product"])
def read_product_by_id(product_id: int, session: Annotated[Session, Depends(db_session)]):
    product = get_product_by_id(session, product_id)
    return product

@app.delete("/delete", tags=["Product"])
def delete_product(product_id: int, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]):
    product = delete_product(session, product_id)
    return product

