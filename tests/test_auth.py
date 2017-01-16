from unittest import TestCase
import json
from bucketlist import *


class TestApiAuthentication(unittest.TestCase):

    def setUp(setUp):
        self.client = bucketlist.app.test_client()
        self.valid_credentials = json.dumps(
            {"username": "kahohi", "password": "ilove@123"})
        self.invalid_credentials = json.dumps(
            {"username": "InvAlid", "password": "ILOVE123"})
        self.wrong_credentials = json.dumps({"username": "", "password": ""})

    def test_registration_with_valid_credentials(self):
        '''Tests that a user is registered successfully'''
        response = self.client.post('bucketlist/api/v1.0/auth/register',
                                    data=self.valid_credentials, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertIn(output["message"], "Registration successful")

    def test_registration_with_unallowed_content(self):
        '''Tests that api does not allow registering with invalid credentials'''
        response = self.client.post('bucketlist/api/v1.0/auth/register',
                                    data=self.wrong_credentials, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        assertIn(output['message'], "Wrong credentials given")

    def test_registrtation_of_already_existing_user(self):
        '''Tests that it does not allow registerig a user alredy exists'''
        response = self.client.post('bucketlist/api/v1.0/auth/register',
                                    data=self.valid_credentials, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response2 = self.client.post('bucketlist/api/v1.0/auth/register',
                                     data=self.valid_credentials, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn(output['messages'], "User already exists")

    def test_registration_only_allows_post_method(self):
        '''Function to ensure that registration only uses post'''
        response = self.client.get('bucketlist/api/v1.0/auth/register')
        self.assertEqual(response.status_code, 405)

    def test_login_with_wrong_credentials(self):
        '''Tests the status code passed when  a user uses either a wrong password or username'''
        response = self.client.post('bucketlist/api/v1.0/auth/register',
                                    data=self.invalid_credentials, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data)
        self.assertIn(output['messages'], "User not found")

    def test_login_only_allows_post(self):
        '''Tests that login anly allows post method'''
        response = self.client.get('bucketlist/api/v1.0/auth/login')
        self.assertEqual(response.status_code, 405)

    def test_passing invalid_content_type(self):
        '''Tests when data passed is not a json'''
        response = self.client.post('bucketlist/api/v1.0/auth/register',
                                    data=["Paul", "password"])
        self.assertEqual(response.status_code, 422)
