from base_tests import BaseTests
import json


class TestApiAuthentication(BaseTests):

    def test_registration_with_valid_credentials(self):
        '''Tests that a user is registered successfully'''
        response = self.client.post('/bucketlist/api/auth/register',
                                    data=self.valid_credentials,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_blank_credentials(self):
        '''Tests that user not allowed to register with blank
           data
        '''
        response = self.client.post('bucketlist/api/auth/register',
                                    data=self.blank_credentials,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_of_already_existing_user(self):
        '''Tests that it does not allow registerig a user alredy exists'''
        response = self.client.post('bucketlist/api/auth/register',
                                    data=self.valid_credentials,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response2 = self.client.post('bucketlist/api/auth/register',
                                     data=self.valid_credentials,
                                     content_type='application/json')
        self.assertEqual(response2.status_code, 400)
        output = json.loads(response2.data)
        self.assertEqual(output['message'], 'user alredy exists')

    def test_registration_only_allows_post_method(self):
        '''Function to ensure that registration only uses post'''
        response = self.client.get('bucketlist/api/auth/register')
        self.assertEqual(response.status_code, 405)

    def test_login_with_valid_credentials(self):
        '''Tests for successful logging in'''
        response = self.client.post('bucketlist/api/auth/register',
                                    data=self.valid_credentials,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response2 = self.client.post('bucketlist/api/auth/login',
                                     data=self.valid_credentials,
                                     content_type='application/json')
        self.assertEqual(response2.status_code, 200)
        output = json.loads(response.data)
        output2 = json.loads(response2.data)
        self.assertEquals(output['message'], 'user created')
        self.assertEqual(output2['message'], 'login successful')

    def test_login_with_wrong_credentials(self):
        '''Tests the status code passed when  a user uses either a
           wrong password or username
        '''
        response = self.client.post('bucketlist/api/auth/register',
                                    data=self.valid_credentials,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response2 = self.client.post('bucketlist/api/auth/login',
                                     data=self.invalid_credentials,
                                     content_type='application/json')
        self.assertEqual(response2.status_code, 401)
        output = json.loads(response2.data)
        self.assertEquals(output['message'],
                          'wrong username/password combination')

    def test_login_only_allows_post(self):
        '''Tests that login anly allows post method'''
        response = self.client.get('bucketlist/api/auth/login')
        self.assertEqual(response.status_code, 405)

    def test_for_user_who_does_not_exist(self):
        '''Tests that a user has to register to login'''
        self.non_existant_user = json.dumps(
            {'username': 'Ivy', 'password': 'sabwani'})
        response = self.client.post('bucketlist/api/auth/login',
                                    data=self.non_existant_user,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'user does not exist')


