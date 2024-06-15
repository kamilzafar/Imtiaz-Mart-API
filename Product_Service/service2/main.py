import io
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from typing import Annotated, List
from fastapi.responses import StreamingResponse
from service2.models import *
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI
from service2 import settings
from uuid import UUID, uuid4
import io
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from typing import Annotated, List
from fastapi.responses import StreamingResponse
from service2.models import *
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI
from service2 import settings
from uuid import UUID, uuid4




@app.get("/", tags=["Root"])
def read_root():
    return {"Service2": "Product Service"}

@app.post("/upload-file", tags=["Image"])
async def get_file(file: Annotated[UploadFile, File(title="Product Image")], session: Annotated[Session, Depends(db_session)]):
    if file.content_type.startswith("image/"):
        try:
            image_data = await file.read()
            image = Image(
                filename=file.filename,
                content_type=file.content_type,
                image_data=image_data
            )
            session.add(image)
            session.commit()
            session.refresh(image)
            return {"id": image.id, "filename": image.filename}
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while saving the image.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

@app.get("/images/{image_id}", tags=["Image"])
def read_image(image_id: int, session: Annotated[Session, Depends(db_session)]):
    image = session.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return StreamingResponse(io.BytesIO(image.image_data), media_type=image.content_type)

@app.post("/products", response_model=Product, tags=["Product"])
def create_product(product: ProductCreate, session: Annotated[Session, Depends(db_session)]):
    product_image = session.get(Image, product.image_id)
    if not product_image:
        raise HTTPException(status_code=400, detail="Image not found")
    product = Product(**product.dict(), id=uuid4())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products", response_model=List[Product], tags=["Product"])
def read_products(session: Annotated[Session, Depends(db_session)], skip: int = 0, limit: int = 10):
    products = session.exec(select(Product).offset(skip).limit(limit)).all()
    return products

@app.get("/products/{product_id}", response_model=Product, tags=["Product"])
def read_product(product_id: UUID, session: Annotated[Session, Depends(db_session)]):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/product/{product_name}", response_model=Product, tags=["Product"])
def get_product_by_name(product_name: str, session: Annotated[Session, Depends(db_session)]):
    product = session.exec(select(Product).where(Product.name.contains(product_name))).all()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/product", tags=["Product"])
def delete_product(product_id: UUID, session: Annotated[Session, Depends(db_session)]):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    image = session.exec(select(Image).where(Image.id == product.image_id)).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    session.delete(product)
    session.commit()
    session.delete(image)
    session.commit()
    return {"message": "Product deleted successfully."}