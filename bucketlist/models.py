
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from Config.config import Config
from __init__ import app
db = SQLAlchemy(app)


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

    def generate_token(self, expiry=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiry)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:  # Correct token but expired time
            return None
        except BadSignature:  # Invalid token
            return None
        user = User.query.get(data['id'])
        return user

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    userlist = db.relationship('BucketList', backref='user', lazy='dynamic')


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    bucketlist_name = db.Column(db.Integer, unique=True)
    bucketlist_Item = db.Column(db.String(50))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.String(10), db.ForeignKey('users.username'))
    bucketowner = db.relationship(
        'BucketListItem', backref='owner_bucket', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


class BucketListItem(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(10))
    bucketlist_name = db.Column(db.String(50),
                                db.ForeignKey('bucketlist.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean)

    def __init__(self, item_name, done):
        self.item_name = item_name
        self.done = done


# Creates the database
db.create_all()
print("sjcbdh")
