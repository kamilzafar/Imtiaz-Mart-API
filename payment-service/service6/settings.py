from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# DATABASE_URL = config("PAYMENT_SERVICE_DATABASE_URL", cast=str)
ORDER_SERVICE_URL = config("ORDER_SERVICE_URL", cast=str)
USER_SERVICE_URL = config("USER_SERVICE_URL", cast=str)
SECRET_KEY_STRIPE = config("SECRET_KEY_STRIPE",cast=str)
WB_SECRET_KEY = config("WB_SECRET_KEY",cast=str)
PRODUCT_SERVICE_URL = config("PRODUCT_SERVICE_URL",cast=str )