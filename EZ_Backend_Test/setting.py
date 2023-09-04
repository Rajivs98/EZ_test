from flask import Flask
from .app_Config.config import ApplicationConfig
# from .handlers.client_handler import mail
# file_path = 'EZ+Backend_Test/handlers/client_file/'
from flask_mail import Mail

def init(app: Flask):
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=ApplicationConfig.DATABASE_URL,
        JWT_SECRET_KEY = ApplicationConfig.FLASK_APP_SECRET_KEY,
        # mail = Mail(app),
        # uploads = 'EZ_Backend_Test/',
        # MAIL_SERVER = 'smtp.gmail.com',
        # MAIL_PORT = 465,
        # MAIL_USERNAME = 'rajivbol979@gmail.com',
        # MAIL_PASSWORD = 'ytuc wetb vkii ekzs',
        # MAIL_TIMEOUT = 30,
        # MAIL_USE_TLS= False,
        # MAIL_USE_SSS= True,
        # mail = Mail(app),
        
    )
