from fastapi import FastAPI
from contextlib import asynccontextmanager
from service5.db import create_db_and_tables
import asyncio
from service5.services import user_consumer_task, order_consumer_task
from service5 import settings
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
   email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_email,
    MAIL_PASSWORD= settings.SMTP_PASSWORD,
    MAIL_PORT=465,
    MAIL_SERVER=settings.smtp_server,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_FROM=settings.smtp_email
)

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

@app.post("/send_mail")
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