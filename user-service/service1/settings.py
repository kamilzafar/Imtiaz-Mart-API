from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("USER_SERVICE_DATABASE_URL", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", cast=str)
KAFKA_BROKER_URL = config("KAFKA_BOOTSTRAP_SERVER", cast=str)
KAFKA_PRODUCER_TOPIC = config("USER_SERVICE_KAFKA_PRODUCER_TOPIC", cast=str)
PRODUCT_SERVICE_URL = config("PRODUCT_SERVICE_URL", cast=str)
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", cast=str)
ORDER_SERVICE_URL = config("ORDER_SERVICE_URL", cast=str)
INVENTORY_SERVICE_URL = config("INVENTORY_SERVICE_URL", cast=str)
PAYMENT_SERVICE_URL = config("PAYMENT_SERVICE_URL", cast=str)