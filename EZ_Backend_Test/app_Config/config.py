from dataclasses import dataclass


@dataclass
class ApplicationConfig(object):
    FLASK_BASE_URL = "http://0.0.0.0:5000"
    FLASK_APP_SECRET_KEY : str = "e42fcf2b00f8d99552d13778d633d16aac27a8a9"
    DATABASE_URL : str = "postgresql://postgres:Sujanix123@localhost:5432/clientOperations_EZ"
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = 'rajivbol979@gmail.com'
    # MAIL_PASSWORD = 'paet aluz oivq xfnp'
    # MAIL_USE_TLS= False
    # MAIL_USE_SSS= True
    

