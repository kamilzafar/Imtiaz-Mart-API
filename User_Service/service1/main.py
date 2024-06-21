from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from service1.curd import signup_user, get_current_user, get_user_by_username, verify_password, check_admin
from service1.db import *
from service1.services import *
from service1.models import *

app = FastAPI(
    title="User Service", 
    description="Manages user authentication, registration, and profiles.",
    version="0.1.0",
    docs_url="/docs", 
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/auth"
    )

@app.get("/", tags=["Root"])
def read_root():
    return {"Service 1": "User Service"}

@app.post("/login", response_model=Token, tags=["Users"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(db_session)]) -> Token:
    user: Userlogin = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": access_token_expires+refresh_token_expires, "token_type": "bearer"}

@app.post("/signup", response_model=User, tags=["Users"])
async def signup(db: Annotated[Session, Depends(db_session)], user: UserCreate ):
    try:
        return signup_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_session)]) -> User:
    user = await get_current_user(token, db)
    return user

@app.patch("/user", response_model=User, tags=["Users"])
def update_user(user: UserUpdate, session: Annotated[Session, Depends(db_session)], current_user: Annotated[User, Depends(get_current_user)]) -> User:
    updated_user = session.exec(select(User).where(User.id == current_user.id)).first()
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        value = value if key != "password" else pwd_context.hash(value)
        setattr(updated_user, key, value)
    session.commit()
    session.refresh(updated_user)
    return updated_user

@app.delete("/user/{username}", response_model=User, tags=["Admin"])
def delete_user(session: Annotated[Session, Depends(db_session)], username: str, current_user: Annotated[User, Depends(check_admin)]) -> User:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_consumer_from_kong(username)
    session.delete(user)
    session.commit()
    return {username: "deleted"}

@app.get("/users", response_model=list[User], tags=["Admin"])
def read_users(db: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(check_admin)]) -> list[User]:
    return db.exec(select(User)).all()