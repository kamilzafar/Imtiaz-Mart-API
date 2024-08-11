from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
ORDER_SERVICE_URL = config("ORDER_SERVICE_URL", cast=str)
SECRET_KEY_STRIPE = config("SECRET_KEY_STRIPE",cast=str)
WB_SECRET_KEY = config("WB_SECRET_KEY",cast=str)