from aiokafka import AIOKafkaConsumer
from service5 import settings
import service5.protobuf.user_pb2 as user
import service5.protobuf.order_pb2 as order
from service5.services import send_email

async def user_consumer_task():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_CONSUMER_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            user_data = user.User()
            user_data.ParseFromString(msg.value)
            subject = "Welcome to KR Mart"
            body = f"Hi {user_data.username},\n\nThank you for signing up with KR Mart!\n\nBest regards,\nKR Mart Team"
            send_email(user_data.email, user_data.username, subject, body)
            print(f"User message processed: {user_data.username}")
    finally:
        await consumer.stop()

async def order_consumer_task():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_ORDER_TOPIC,  # Replace with your actual order topic
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_ORDER_GROUP_ID,
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            order_data = order.Order()  # Assuming you have an Order message in order.proto
            order_data.ParseFromString(msg.value)
            subject = "Order Confirmation"
            body = f"Hi {order_data.username},\n\nYour order {order_data.order_id} has been placed successfully!\n\nBest regards,\nKR Mart Team"
            send_email(order_data.useremail, order_data.username, subject, body)
            print(f"Order message processed: {order_data.order_id}")
    finally:
        await consumer.stop()