from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from app import db
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import JSON


class Users(db.Model):
    __tablename__ = 'users'
    _id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('Email', db.String(100))
    password = db.Column('Password', db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def get_token(self, expires_sec=600):
        serial = Serializer(current_app.config['SECRET_KEY'])
        payload = {
            'user_id': self._id,
            'exp': (datetime.utcnow() + timedelta(seconds=expires_sec)).timestamp()
        }
        return serial.dumps(payload)
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


class Cars(db.Model):
    __tablename__ = 'cars'
    _id = db.Column('id', db.Integer, primary_key=True)
    car_type = db.Column(db.String(100))
    content = db.Column(JSON)

    def __init__(self, car_type, content):
        self.car_type = car_type
        self.content = content


class Images(db.Model):
    __tablename__ = 'images'
    _id = db.Column('id', db.Integer, primary_key=True)
    image_name = db.Column(db.String(100))
    image_file_path = db.Column(JSON)


class Title_info(db.Model):
    __tablename__ = 'info'
    _id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id': self._id,
            'title': self.title,
            'description': self.description
        }