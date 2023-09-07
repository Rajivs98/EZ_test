from dataclasses import dataclass

@dataclass
class ApplicationConfig(object):
    FLASK_BASE_URL = "http://0.0.0.0:5000"
    FLASK_APP_SECRET_KEY : str = "e42fcf2b00f8d99552d13778d633d16aac27a8a9"
    DATABASE_URL : str = "postgresql://postgres:Sujanix123@localhost:5432/clientOperationsEZ"
    uploads = 'EZ_Backend_Test/'
    MAIL_SERVER : str = 'smtp.gmail.com'
    MAIL_PORT : int = 465
    MAIL_USERNAME : str = 'rajivbol979@gmail.com'
    MAIL_PASSWORD : str = 'ytuc wetb vkii ekzs'
    MAIL_USE_TLS : bool = False
    MAIL_USE_SSS : bool = True
    # mail = mail
    

    

