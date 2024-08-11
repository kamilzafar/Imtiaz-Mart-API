from sqlmodel import SQLModel, create_engine, Session
from service3 import setting

connection_string = str(setting.DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def db_session():
    with Session(engine) as session:
        yield session