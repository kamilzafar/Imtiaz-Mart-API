from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer, Consumer, KafkaError
import asyncio

app = FastAPI()

# Kafka Producer Configuration
producer_conf = {'bootstrap.servers': 'broker:9092'}
producer = Producer(producer_conf)

# Kafka Consumer Configuration
consumer_conf = {
    'bootstrap.servers': 'broker:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['my_topic'])

class Item(BaseModel):
    name: str
    value: str

@app.get("/")
def get_root():
    return {"service6": "Payment Service"}

@app.post("/produce/")
async def produce_message(item: Item):
    producer.produce('my_topic', key=item.name, value=item.value)
    producer.flush()
    return {"status": "message produced"}

@app.get("/consume/")
async def consume_message():
    messages = []
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                return {"error": msg.error()}
            continue
        messages.append({
            "key": msg.key().decode('utf-8'),
            "value": msg.value().decode('utf-8')
        })
    return {"messages": messages}

@app.on_event("shutdown")
def shutdown_event():
    consumer.close()
