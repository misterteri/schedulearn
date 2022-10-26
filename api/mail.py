from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME = "scheduledeeplearning",
    MAIL_PASSWORD = "pnrdkxwgtnodewrf",
    MAIL_FROM = "scheduledeeplearning@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Schedulearn",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(email: str):
    html = """A user is trying to sign in on Schedulearn, but user does not exist """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html
    )

    fm = FastMail(conf)
    await fm.send_message(message)