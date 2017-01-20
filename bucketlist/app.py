from flask import Flask
from flask_restful import Api, Resource, reqparse
from models import User
from __init__ import app
api = Api(app)


class RegisterApi(Resource):

    def post(self):
        '''Receives credentials and registers a new user using
           using a username and a password
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help="Username cannot be blank")
        parser.add_argument('password', required=True,
                            help="Password cannot be blank")
        credentials = parser.parse_args()
        uname = credentials['username']
        pword = credentials['password']
        user = User(username=uname, password=pword)
        # Hashes the password
        user.hash_password(pword)
        # Adds to the database
        user.add(user)
        return ({'message': 'user created'}, 201)


class LoginApi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help="Username cannot be blank")
        parser.add_argument('password', required=True,
                            help="Password cannot be blank")
        credentials = parser.parse_args()
        uname = credentials['username']
        pword = credentials['password']

        # confirm that the user does exist
        user = User.query.filter_by(username=uname).first()
        if user is None:
            return({'message': 'user does not exist'})
        else:
            # verify the password
            if user.veriry_password(pword, user.password):
                return({'message': 'Login successful'}, 200)
            else:
                return({'message': 'wrong password', 'passcode':user.password}, 400)


class BucketLists(Resource):
    def get(self):
        pass

    def post(self):
        pass


class BucketList(Resource):
    def get(self, id):
        pass

    def post(self, id):
        pass

    def delete(self, id):
        pass


class BucketListItems(Resource):
    def post(self, id):
        pass


class BucketListItem(Resource):
    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(RegisterApi, '/bucketlist/api/auth/register')

api.add_resource(LoginApi, '/bucketlist/api/auth/login', )

api.add_resource(BucketLists, '/bucketlist/api/bucketlists',)
api.add_resource(
    BucketList, '/bucketlist/api/bucketlists/<int:id>', )

api.add_resource(
    BucketListItems, '/bucketlist/api/bucketlists/<int:id>/items', )

api.add_resource(
    BucketListItem, '/bucketlist/api/bucketlists/<int:id>/items/<int:item_id>', )


if __name__ == '__main__':
    app.run(debug=True)
