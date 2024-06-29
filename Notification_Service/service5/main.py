from fastapi import FastAPI
from contextlib import asynccontextmanager
from service5.db import create_db_and_tables
import asyncio
from service5.services import consumer_task, send_email
from service5 import settings
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
   email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME="kamilzafar54@gmail.com",
    MAIL_PASSWORD= settings.SMTP_PASSWORD,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_FROM="kamilzafar65@gmail.com"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    asyncio.create_task(consumer_task(settings.KAFKA_CONSUMER_TOPIC, settings.KAFKA_BROKER_URL))
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

@app.post("/send_mail")
async def send_mail(email: EmailSchema):
 
    template = """
        <html>
        <body>
         
 
        <p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
 
        </body>
        </html>
        """
 
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)     
 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})