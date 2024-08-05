from aiokafka import AIOKafkaProducer
from service1 import settings

async def produce_message():
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URL)
    await producer.start()
    try:
        # Produce message
        yield producer
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()