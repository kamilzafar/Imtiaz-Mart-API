from sqlmodel import SQLModel, create_engine, Session
from service5 import settings

# Create the database engine
connection_string = str(settings.DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)
# Create the database session
def db_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)