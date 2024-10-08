from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("INVENTORY_SERVICE_DATABASE_URL", cast=str)
USER_SERVICE_URL = config("USER_SERVICE_URL", cast=str)
PRODUCT_SERVICE_URL = config("PRODUCT_SERVICE_URL", cast=str)
ORDER_SERVICE_URL = config("ORDER_SERVICE_URL", cast=str)