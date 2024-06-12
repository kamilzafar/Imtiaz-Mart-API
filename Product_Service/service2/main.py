from fastapi import FastAPI

app = FastAPI(
    title="Product Service",
    description="Manages product catalog, including CRUD operations for products.",
    version="0.1"
)

@app.get("/")
def read_root():
    return {"Service2": "Product Service"}