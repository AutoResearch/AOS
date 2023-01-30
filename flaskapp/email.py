from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask_mail import Mail, Message
from threading import Thread
import os

EMAIL_KEY = os.environ.get("EMAIL_KEY")
VERIFY_EMAIL_SALT = os.environ.get("VERIFY_EMAIL_SALT")
RESET_SALT = os.environ.get("RESET_SALT")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USERNAME": SENDER_EMAIL,
    "MAIL_PASSWORD": EMAIL_PASSWORD,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
}

mail = Mail()
serializer = URLSafeTimedSerializer(EMAIL_KEY)

EXPIRED = "EXPIRED"


def generate_token(email, salt):
    return serializer.dumps(email, salt)


def _send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_token_email(app, email, subject, template):
    msg = Message(subject, recipients=[email], html=template, sender=SENDER_EMAIL)
    Thread(target=_send_mail_async, args=(app, msg)).start()


def confirm_token(token, salt):
    try:
        email = serializer.loads(token, salt=salt)
        serializer.loads(token, salt=salt, max_age=600)
    except SignatureExpired:
        # should we have an easier resend procedure if link is expired?
        email = EXPIRED
    except BadSignature:
        email = ""
    return email
