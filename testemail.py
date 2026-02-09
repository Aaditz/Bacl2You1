from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="aaditzsharma416@gmail.com",
    MAIL_PASSWORD="gwzp fqat xnja slmp"
)

mail = Mail(app)

with app.app_context():
    msg = Message(
        subject="Test Email",
        sender=app.config['MAIL_USERNAME'],
        recipients=["25mscs01@kristujayanti.com"],  # test sending to yourself
        body="Hello, this is a test email from Flask!"
    )
    try:
        mail.send(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)
