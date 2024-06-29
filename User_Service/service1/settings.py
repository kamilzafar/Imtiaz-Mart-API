from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", cast=str)
KONG_ADMIN_URL = config("KONG_ADMIN_URL", cast=str)
KAFKA_BROKER_URL = config("KAFKA_BROKER_URL", cast=str)
KAFKA_PRODUCER_TOPIC = config("KAFKA_PRODUCER_TOPIC", cast=str)