from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

KAFKA_GROUP_ID = config("NOTIFICATION_SERVICE_KAFKA_GROUP_ID", cast=str)
KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER", cast=str) 
KAFKA_CONSUMER_TOPIC = config("NOTIFICATION_SERVICE_KAFKA_CONSUMER_TOPIC", cast=str)
smtp_server = config("SMTP_SERVER", cast=str)
smtp_port = config("SMTP_PORT", cast=int)
smtp_email = config("SMTP_EMAIL", cast=str)
smtp_username = config("SMTP_USERNAME", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str)
KAFKA_ORDER_TOPIC = config("NOTIFICATION_SERVICE_KAFKA_ORDER_TOPIC", cast=str)
KAFKA_ORDER_GROUP_ID = config("NOTIFICATION_SERVICE_KAFKA_ORDER_GROUP_ID", cast=str)