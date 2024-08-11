from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("ORDER_SERVICE_DATABASE_URL", cast=str)
KAFKA_BOOTSTRAP_SERVER = config("ORDER_SERVICE_KAFKA_BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("ORDER_SERVICE_KAFKA_ORDER_TOPIC", cast=str)
USER_SERVICE_URL = config("USER_SERVICE_URL", cast=str)
PRODUCT_SERVICE_URL = config("PRODUCT_SERVICE_URL", cast=str)
INVENTORY_SERVICE_URL = config("INVENTORY_SERVICE_URL", cast=str)