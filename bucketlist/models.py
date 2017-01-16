from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config('DATABASE_URI')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    userlist = db.relationship('BucketList', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class BucketList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bucketlist_name = db.Column(db.Integer, unique=True)
    bucketlist_Item = db.Column(db.String(50))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.String(10), db.ForeignKey('user.username'))
    bucketowner = db.relationship(
        'BucketListItem', backref='owner_bucket', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


class BucketListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(10))
    bucketlist_name = db.Column(db.String(50), db.ForeignKey('owner_bucket.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean)

    def __init__(self, item_name, done):
        self.item_name = item_name
        self.done = done

#Creates the database
db.create_all()