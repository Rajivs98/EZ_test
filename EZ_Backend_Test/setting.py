from flask import Flask
from .app_Config.config import ApplicationConfig
# file_path = 'EZ+Backend_Test/handlers/client_file/'

def init(app: Flask):
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=ApplicationConfig.DATABASE_URL,
        JWT_SECRET_KEY = ApplicationConfig.FLASK_APP_SECRET_KEY,
        uploads = ApplicationConfig.uploads,
        MAIL_SERVER = ApplicationConfig.MAIL_SERVER,
        MAIL_PORT = ApplicationConfig.MAIL_PORT,
        MAIL_USERNAME = ApplicationConfig.MAIL_USERNAME,
        MAIL_PASSWORD = ApplicationConfig.MAIL_PASSWORD,
        MAIL_USE_TLS= ApplicationConfig.MAIL_USE_TLS,
        MAIL_USE_SSS= ApplicationConfig.MAIL_USE_SSS,
        MAIL_TIMEOUT = 30,
        # mail = ApplicationConfig.mail()
        # uploads = 'EZ_Backend_Test/',
        # MAIL_SERVER = 'smtp.gmail.com',
        # MAIL_PORT = 465,
        # MAIL_USERNAME = 'rajivbol979@gmail.com',
        # MAIL_PASSWORD = 'ytuc wetb vkii ekzs',
        # MAIL_TIMEOUT = 30,
        # MAIL_USE_TLS= True,
        # MAIL_USE_SSS= False,
        
    )
