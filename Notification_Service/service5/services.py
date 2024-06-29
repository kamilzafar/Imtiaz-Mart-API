from aiokafka import AIOKafkaConsumer
from service5 import settings
import service5.user_pb2 as user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def send_email(email, name):
    # SMTP configuration
    smtp_server = settings.smtp_server
    smtp_port = settings.smtp_port
    # smtp_user = settings.smtp_email
    smtp_user = settings.smtp_email
    smtp_password = settings.SMTP_PASSWORD

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Welcome to Imtiaz Mart"

    body = f"Hi {name},\n\nThank you for signing up with Imtiaz Mart!\n\nBest regards,\nImtiaz Mart Team"
    msg.attach(MIMEText(body, 'plain'))
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server using a secure context
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def consumer_task(name: str, server: str):
    consumer = AIOKafkaConsumer(
        name,
        bootstrap_servers=server,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset='earliest'  
    )
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            user_data = user.User()
            user_data.ParseFromString(msg.value)
            message = str(user_data.username)
            send_email(user_data.email, user_data.username)
            print(f"message: {message}")
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()