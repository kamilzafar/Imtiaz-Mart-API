from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer
from typing import Annotated, List
from service2.models import *
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI
from service2 import settings
from uuid import UUID, uuid4
import io

connection_string = str(settings.DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

# Create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

def db_session():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="Product Service",
    description="Manages product catalog, including CRUD operations for products.",
    version="0.1",
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/product",
    docs_url="/docs"
)

auth_scheme = HTTPBearer()

@app.middleware("http")
async def verify_jwt(request: Request, call_next):
    if request.url.path not in ["/docs", "/openapi.json", "/products"]:
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        try:
            payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"message": "Token has expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"message": "Invalid token"})
    response = await call_next(request)
    return response


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

@app.post("/product", response_model=Product, tags=["Product"])
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

@app.get("/products/{product_name}", response_model=Product, tags=["Product"])
def get_product_by_name(product_name: str, session: Annotated[Session, Depends(db_session)]):
    product = session.exec(select(Product).where(Product.name.contains(product_name))).all()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/product/{product_id}", tags=["Product"])
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