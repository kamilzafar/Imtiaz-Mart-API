from fastapi import FastAPI
from contextlib import asynccontextmanager
from service5.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    yield

app = FastAPI(
    title="Notification Service", 
    description=" Sends notifications (email, SMS) to users about order statuses and other updates.",
    version="0.1.0",
    docs_url="/docs", 
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/notification"
    )

@app.get("/", tags=["Root"])
def read_root():
    return {"Service": "Notification Service"}