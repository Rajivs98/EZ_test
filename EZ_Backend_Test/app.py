from flask import Flask
from .blueprints import client_blueprint
from .handlers.client_handler import mail
from . import db
from . import setting
from flask_jwt_extended import JWTManager
# from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    # CORS(app)
    setting.init(app)
    db.init_app(app)
    JWTManager(app)
    mail.init_app(app)
    app.register_blueprint(client_blueprint.blueprint, url_prefix='/ez')

    return app

