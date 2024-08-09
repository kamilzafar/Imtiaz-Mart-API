from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
ORDER_SERVICE_URL = config("ORDER_SERVICE_URL", cast=str)