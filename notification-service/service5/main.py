from fastapi import FastAPI,Request,HTTPException
from contextlib import asynccontextmanager
import asyncio
from service5.kafka.consumers import user_consumer_task, order_consumer_task
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from service5.models.email_model import EmailSchema
from service5.services import conf,send_email
from service5.protobuf import user_pb2



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
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


@app.post("/user_service")
async def handle_user_signup(request: Request):
    try:
        data = await request.body()

        # Parse the protobuf message
        user_message = user_pb2.User()
        user_message.ParseFromString(data)

        # Extract details and send an email
        email = user_message.email
        name = user_message.username
        subject = "Welcome to KR Mart"
        body = f"Hi {name},\n\nThank you for signing up with KR Mart!\n\nBest regards,\nKR Mart Team"

        send_email(email=email, name=name, subject=subject, body=body)

        return {"status": "Email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



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