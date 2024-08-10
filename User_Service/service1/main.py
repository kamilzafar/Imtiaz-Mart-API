from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from service1.kafka.producer import produce_message
from service1.crud.user_crud import user_login, update_user, delete_user, signup_user, signup_user, get_current_user, check_admin
from service1.database.db import *
from service1.services import *
from service1.models.user_models import *
from fastapi.middleware.cors import CORSMiddleware
from service1.settings import ORDER_SERVICE_URL, INVENTORY_SERVICE_URL, PRODUCT_SERVICE_URL, NOTIFICATION_SERVICE_URL, PAYMENT_SERVICE_URL

app = FastAPI(
    title="User Service", 
    description="Manages user authentication, registration, and profiles.",
    version="0.1.0",
    lifespan=lifespan,
    root_path="/auth"
    )

origins = [
    ORDER_SERVICE_URL,
    INVENTORY_SERVICE_URL,
    PRODUCT_SERVICE_URL,
    NOTIFICATION_SERVICE_URL,
    PAYMENT_SERVICE_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"service": "User Service"}

@app.post("/login", response_model=Token, tags=["User"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(db_session)]) -> Token:
    user = user_login(db, form_data)
    return user

@app.post("/signup", response_model=User, tags=["User"])
async def signup(db: Annotated[Session, Depends(db_session)], user: UserCreate, producer: Annotated[AIOKafkaProducer, Depends(produce_message)]):
    try:
        return await signup_user(user, db, producer)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.get("/users/me", response_model=User, tags=["User"])
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_session)]) -> User:
    user = await get_current_user(token, db)
    return user

@app.patch("/update-user", response_model=User, tags=["User"])
def update_user(user: UserUpdate, session: Annotated[Session, Depends(db_session)], current_user: Annotated[User, Depends(get_current_user)]) -> User:
    updated_user = update_user(user, session, current_user)
    return updated_user

@app.delete("/delete-user", response_model=User, tags=["User"])
def user_delete(session: Annotated[Session, Depends(db_session)], current_user: Annotated[User, Depends(get_current_user)]):
    delete_user(session, current_user.username)
    return {"message": "User deleted successfully"}

@app.get("/users", response_model=list[User], tags=["Admin"])
def read_users(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]) -> list[User]:
    return db.exec(select(User)).all()