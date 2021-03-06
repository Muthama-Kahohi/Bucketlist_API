from bucketlist import create_app, db
from flask import json
import unittest
from bucketlist.app import *


class BaseTests(unittest.TestCase):
    '''
       Purpose of this class is to set up all the dat that will be requit=red to run tests.
       This will include a registered user and a token for all methods that will required 
       a user to be logged in
    '''

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.valid_credentials = json.dumps(
            {"username": "kahohi", "password": "ilove@123"})
        self.invalid_credentials = json.dumps(
            {"username": "kahohi", "password": "ILOVE123"})
        self.blank_credentials = json.dumps({"username": '', 'password': ''})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
