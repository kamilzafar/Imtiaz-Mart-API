from fastapi import FastAPI

app = FastAPI(docs_url="/docs")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/service1")
def read_service1():
    return {"service": "service1"}

