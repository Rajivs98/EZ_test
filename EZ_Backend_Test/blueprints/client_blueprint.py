from flask.blueprints import Blueprint
from ..handlers.client_handler import Client_handler
from ..models.client_model import client
from flask import request, jsonify
from flask_login import login_required, login_user, logout_user
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


blueprint = Blueprint('ez_blueprint',__name__)


@blueprint.route('/register', methods=['POST'])
def register():
    return Client_handler(request.json).handle()
 
@blueprint.route('/login', methods=['POST'])
def login():
    return Client_handler(request.json).login_user()

@blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = client.query.get(current_user_id)
    return jsonify({"message": "This is a protected route", "user": user.username}), 200


@blueprint.route('/logout', methods=['GET'])
@jwt_required()
def logout(): 
    return Client_handler(request.json).logout_user()

@blueprint.route('/sendmail', methods=['GET', 'POST'])
@jwt_required()
def sendmail():
    return Client_handler(request.json).send_verification_email()

@blueprint.route('/verifyemail', methods=['POST'])
@jwt_required()
def verify_email():
    return Client_handler(request.json).email_verify()

@blueprint.route('/uploadfile', methods=['POST'])
@jwt_required()
def uploadfile():
    return Client_handler(request.json).upload_file()

@blueprint.route('/downloadfile/<filename>', methods=['GET'])
@jwt_required()
def downloadfile(filename):
    return Client_handler(request.json).download_file(filename)


@blueprint.route('/listallfile', methods=['GET'])
@jwt_required()
def list_all_file():
    return Client_handler(request.json).list_uploaded_files()

