from base_tests import BaseTests
import json


class test_bucketlists(BaseTests):
    def get_token(self):
        response = self.client.post('/bucketlist/api/auth/register',
                                    data=self.valid_credentials,
                                    content_type='application/json')
        response2 = self.client.post('/bucketlist/api/auth/login',
                                     data=self.valid_credentials,
                                     content_type='application/json')
        output = json.loads(response2.get_data())
        token = output.get('Authorization')
        return {'Authorization': 'Token ' + token}

    def test_successful_creation_of_a_bucketlist(self):
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=self.get_token())
        self.assertEqual(create_bucketlist.status_code, 201)
        output = json.loads(create_bucketlist.data)
        self.assertEqual(output['message'], 'Bucketlist successfully created')

    def test_creation_of_already_existing_bucketlist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 201)

        create_bucketlist2 = self.client.post('bucketlist/api/bucketlists',
                                              data=self.bucket,
                                              content_type='application/json',
                                              headers=token)

        self.assertEqual(create_bucketlist2.status_code, 400)
        output = json.loads(create_bucketlist2.data)
        self.assertEqual(output['message'], 'Bucketlist already exists')

    def test_getting_of_all_bucketlists(self):
        get_bucketlists = self.client.get('bucketlist/api/bucketlists',
                                          headers=self.get_token())
        self.assertEquals(get_bucketlists.status_code, 200)

    def test_accessing_bucketlist_without_logging_in(self):
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json')
        self.assertEqual(create_bucketlist.status_code, 401)

    def test_creating_bucketlist_with_blank_name(self):
        self.bucket = json.dumps(
            {'Bucketname': ''})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=self.get_token())
        self.assertEqual(create_bucketlist.status_code, 400)
        output = json.loads(create_bucketlist.data)
        self.assertEqual(output['message'], 'Bucketlist name cannot be blank')

    def test_deleting_bucketlist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 201)
        delete_bucketlist = self.client.delete('bucketlist/api/bucketlists/1',
                                               content_type='application/json',
                                               headers=token)
        self.assertEqual(delete_bucketlist.status_code, 200)

    def test_deleting_bucketlist_that_does_not_exist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 201)
        delete_bucketlist = self.client.delete('bucketlist/api/bucketlists/2',
                                               content_type='application/json',
                                               headers=token)
        self.assertEqual(delete_bucketlist.status_code, 400)
        output = json.loads(delete_bucketlist.data)
        self.assertEqual(output['message'], 'Bucketlist does not exist')

    def test_getting_specific_bucketlist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 201)
        get_bucketlist = self.client.get('bucketlist/api/bucketlists/1',
                                         content_type='application/json',
                                         headers=token)
        self.assertEqual(get_bucketlist.status_code, 200)

    def test_updating_a_bucketlist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Functionality'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 200)
        self.update = json.dumps(
            {'Bucketname': 'Add Bucketlist Functionality'})
        update_bucketlist = self.client.put('bucketlist/api/bucketlists/1',
                                            data=self.update,
                                            content_type='application/json',
                                            headers=token)
        self.assertEqual(update_bucketlist.status_code, 200)

    def test_getting_a_bucketlist_that_does_not_exist(self):
        token = self.get_token()
        self.bucket = json.dumps(
            {'Bucketname': 'Handling Authentication Tests'})
        create_bucketlist = self.client.post('bucketlist/api/bucketlists',
                                             data=self.bucket,
                                             content_type='application/json',
                                             headers=token)
        self.assertEqual(create_bucketlist.status_code, 201)
        get_bucketlist = self.client.get('bucketlist/api/bucketlists/2',
                                         content_type='application/json',
                                         headers=token)
        self.assertEqual(get_bucketlist.status_code, 400)
        output = json.loads(get_bucketlist.data)
        self.assertEqual(output['message'], 'Bucketlist doe not exist')