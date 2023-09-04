from ..models.client_model import client, UploadedFile, Verification_Table
from dataclasses import dataclass
from flask import request, jsonify, send_file, Flask
from ..db import db
from flask_mail import Mail, Message
from typing import Dict
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, get_jwt_identity, decode_token
import os
from .utils import generate_otp


blacklist = set()
mail = Mail()

@dataclass
class client_request_body:
    name: str
    username: str
    password: str
    email: str
    phone: str
    address: str
    role : str
    otp : str

    def __init__(self, request_dict: Dict):
        for k, v in request_dict.items():
            setattr(self, k, v)


class Client_handler:
    request: client_request_body

    def __init__(self, request: Dict):
        self.request = client_request_body(request)

    def handle(self):
        try:
            if (client.query.filter_by(username=self.request.username).first()) is not None: 
                return jsonify({"message": "Username already exists"})
            else:
                return self.singup_user()

        except Exception as e:
            return jsonify({"error": str(e)})


    def singup_user(self):
        try:
            #   if client.query.filter_by(username=username).first() is not None:
            #       return jsonify({"message": "Username already exists"})
            #         user = client(username=username, password_hash=generate_password_hash(password))
            otp = self.send_verification_email()
            data = client(
                name=self.request.name,
                username=self.request.username,
                password=generate_password_hash(self.request.password),
                email=self.request.email,
                phone=self.request.phone,
                address=self.request.address,
                role=self.request.role,
            )
            send_ver = Verification_Table(
                email = self.request.email,
                otp = otp,
                verified = False
            )
            db.session.add(data)
            db.session.add(send_ver)
            db.session.commit()

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})
        
    def login_user(self):
        try:
            uname = self.request.username
            passw = self.request.password
            user = client.query.filter_by(username=uname).first()
            if user is None:
                return jsonify({"res": "user not found"})
            elif user and user.role == 'client':
                if not check_password_hash(user.password, passw):
                    return jsonify({"res": "invalid password"})
                else:
                    access_token = create_access_token(identity=user.id, expires_delta=False)
                    
                return jsonify({"res": "Login Successful", "access_token": access_token}), 200
            else:
                return jsonify({"res": "you are not authorized"})
        except Exception as e:
            return jsonify({"error": str(e)})

    
    def logout_user():
        # blacklist = set() 
        try: 
            auth_header = request.headers.get('Authorization')
            if auth_header:
                current_token = auth_header.split()[1]
                token_info = decode_token(current_token)
                jti = token_info['jti']
                blacklist.add(jti)
                blacklist_as_list = list(blacklist)
                print("blacklist", blacklist_as_list)
                return jsonify({"resp":"Logout Successful"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def send_verification_email(self):
        try:
            otp = generate_otp()
            app = Flask(__name__)
            app.config['MAIL_SERVER']='smtp.gmail.com'
            app.config['MAIL_PORT'] = 465
            app.config['MAIL_USERNAME'] = 'rajivbol979@gmail.com'
            app.config['MAIL_PASSWORD'] = 'ytuc wetb vkii ekzs'
            app.config['MAIL_USE_TLS'] = False
            app.config['MAIL_USE_SSL'] = True
            mail = Mail(app)
            msg = Message(f"{self.request.name}", sender="rajivbol979@gmail.com", recipients=[f"{self.request.email}"])
            msg.body = f"Your verification code is {otp}"
            mail.send(msg)
            # return jsonify("Message sent successfully")
            return otp
        except Exception as e:
            return jsonify({"error": str(e)})

    def email_verify(self):
        try:
            email = self.request.email
            otp = self.request.otp
            user = Verification_Table.query.filter_by(email=email).first()
            if user is None:
                return jsonify({"res": "invalid email"})
            elif user and user.otp == otp :
                user.verified=True
                db.session.commit()
                return jsonify({"res": "email verified successfully"})
            else:
                return jsonify({"res": "Invalid otp"})
        
        except Exception as e:
            return jsonify({"error": str(e)})
    

    def upload_file():
        try:
            accept = ('pptx', 'docx', 'xlsx', 'pdf')
            # file_path = 'C:/Users/payfi/Desktop/FlaskProject/EZ_Assesment/EZ_Backend_Test/handlers/client_file/'
            file = request.files['file']
            print(file)
            username=request.form.get('username')
            if file is None or file.filename == '':
                return jsonify({'resp': 'no file found'})
            filename = file.filename
            file_path = 'handlers/client_file/'
            if file and (filename.split('.')[1]).lower() in accept:
                # files = filename
                filename = secure_filename(file.filename)
                file_path = os.path.join(file_path, filename)
                file.save(file_path)
                # with open(f'handlers/client_file/{username}{filename}', 'w+') as file:
                #     file.write('')
                #     file.close()
                filedata = UploadedFile(
                    filename = filename,
                    username = username,
                    file_path = file_path,
                )
                db.session.add(filedata)
                db.session.commit()

                return jsonify({'resp': 'file uploaded successfully'})
            else:
                return jsonify({'resp': 'file upload failed'})
        except Exception as e:
            return jsonify({'error': str(e)})
    

    def download_file(filename):
        try:
            # user = client.query.filter(client.role=='admin').first()
            # # user = current_user
            # if user != "client":
            #     return jsonify({"resp": "you can't download this file"})
            file = UploadedFile.query.filter_by(filename=filename).first()
            if file is None:
                return jsonify({"resp": "File not found"})
            else:
                file_path = file.file_path
                return send_file(file_path, as_attachment=True)
        except Exception as e:
            return jsonify({"resp":str(e)})
    
    def list_uploaded_files():
        try:
            uploaded_files = UploadedFile.query.all()
            file_list = [i.filename for i in uploaded_files]
            return jsonify({"file_list": file_list})
        except Exception as e:
            return jsonify({'error': str(e)})