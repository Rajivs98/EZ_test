from nanoid import generate
from flask import Flask, jsonify, request
from flask_mail import Mail, Message


def generate_otp():
    return generate("1234567890", 6)

mail = Mail()
def send_email(self):
    try:
        otp = generate_otp()
        app = Flask(__name__)
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'rajivbol979@gmail.com'
        app.config['MAIL_PASSWORD'] = 'ytuc wetb vkii ekzs'
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)
        msg = Message(f"{request.json['name']}", sender="rajivbol979@gmail.com",
                      recipients=[f"{request.json['email']}"])
        msg.body = f"Your verification code is {otp}"
        mail.send(msg)
        # return jsonify("Message sent successfully")
        return otp
    except Exception as e:
        return jsonify({"error": str(e)})
