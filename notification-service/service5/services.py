import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from service5 import settings
from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_email,
    MAIL_PASSWORD= settings.SMTP_PASSWORD,
    MAIL_PORT=465,
    MAIL_SERVER=settings.smtp_server,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_FROM=settings.smtp_email
)

def send_email(email, name, subject, body):
    smtp_server = settings.smtp_server
    smtp_port = settings.smtp_port
    smtp_user = settings.smtp_email
    smtp_password = settings.SMTP_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
