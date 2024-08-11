from fastapi import FastAPI
from contextlib import asynccontextmanager
from service5.database.db import create_db_and_tables
import asyncio
from service5.kafka.consumers import user_consumer_task, order_consumer_task
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from service5.models.email_model import EmailSchema
from service5.services import conf

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    asyncio.create_task(user_consumer_task())
    asyncio.create_task(order_consumer_task())
    yield

app = FastAPI(
    title="Notification Service", 
    description="Sends notifications (email, SMS) to users about order statuses and other updates.",
    version="0.1.0",
    lifespan=lifespan,
    root_path="/notification"
    )

@app.get("/", tags=["Root"])
def read_root():
    return {"service": "Notification Service"}

@app.post("/send_mail", tags=["Email"])
async def send_mail(email: EmailSchema):

    body = f"Hi! ,\n\nYour order has been placed successfully!\n\nBest regards,\nKR Mart Team"
 
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=body,
        subtype="plain"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)     
 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})