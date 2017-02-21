
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.hash import pbkdf2_sha256
from Config.config import Config
from bucketlist import db
from datetime import datetime


class CRUD():
    '''
       Class to add, update and delete data via SQLALchemy sessions
    '''

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class User(db.Model, CRUD):
    '''defines user columns     '''
    __tablename__ = 'users'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, passcode):
        '''Password hashing to avoid saving password in plain text'''
        self.password = pbkdf2_sha256.hash(passcode)

    def veriry_password(self, password, db_passcode):
        return pbkdf2_sha256.verify(password, db_passcode)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    userlist = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def generate_token(self, expiry=60000):
        s = Serializer(Config.SECRET_KEY, expires_in=expiry)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_authentication_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Bucketlist(db.Model, CRUD):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    bucketlist_name = db.Column(db.Integer, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.String(10), db.ForeignKey('users.username'))
    bucketowner = db.relationship(
        'BucketListItem', backref='owner_bucket', lazy='dynamic')
    items = db.relationship('BucketListItem',
                            backref='bucketlist',
                            passive_deletes=True)


class BucketListItem(db.Model, CRUD):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(10))
    bucketlist_name = db.Column(db.Integer,
                                db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=datetime.utcnow)
    done = db.Column(db.Boolean)

