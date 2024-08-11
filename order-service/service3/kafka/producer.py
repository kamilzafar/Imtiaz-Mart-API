from aiokafka import AIOKafkaProducer
from service3 import setting

async def produce_message():
    producer = AIOKafkaProducer(bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVER)
    await producer.start()
    try:
        # Produce message
        yield producer
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()