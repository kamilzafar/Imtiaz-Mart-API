from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
USER_SERVICE_URL = config("USER_SERVICE_URL", cast=str)
INVENTORY_SERVICE_URL = config("INVENTORY_SERVICE_URL", cast=str)