from dataclasses import dataclass
from ..db import db


@dataclass
class client(db.Model):
    __tablename__ = 'client'

    id: int
    name: str
    username : str
    password: str
    email: str
    phone: str
    address: str
    role : str

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)


@dataclass
class UploadedFile(db.Model):
    __tablename__ = 'client_files'
    __allow_unmapped__ = True

    id : int
    filename : str
    username : str
    file_path : str

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)


@dataclass
class Verification_Table(db.Model):
    __tablename__ = 'verification'
    __allow_unmapped__ = True

    id = int
    email = str
    otp = str
    verified = bool

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    otp = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)