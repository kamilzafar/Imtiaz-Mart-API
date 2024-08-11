from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
KAFKA_GROUP_ID = config("KAFKA_GROUP_ID", cast=str)
KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER", cast=str) 
KAFKA_CONSUMER_TOPIC = config("KAFKA_CONSUMER_TOPIC", cast=str)
smtp_server = config("smtp_server", cast=str)
smtp_port = config("smtp_port", cast=int)
smtp_email = config("smtp_email", cast=str)
smtp_username = config("smtp_username", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_ORDER_GROUP_ID = config("KAFKA_ORDER_GROUP_ID", cast=str)