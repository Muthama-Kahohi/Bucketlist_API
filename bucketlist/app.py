from flask_restful import Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from bucketlist.models import User, BucketList
from sqlalchemy import exc
from flask import g

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token):
    # Authenticating the token
    user = User.verify_token(token)
    if not user:
        return False
    g.user = user
    return True


class RegisterApi(Resource):

    def post(self):
        '''Receives credentials and registers a new user using
           using a username and a password
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', required=True,
                                help="Username cannot be blank")
            parser.add_argument('password', required=True,
                                help="Password cannot be blank")
            credentials = parser.parse_args()
            uname = credentials['username']
            pword = credentials['password']
            # Ensure that registration details are not blank
            if len(uname) <= 0 or len(pword) <= 0:
                return({'message': 'please provide all credentials'}, 400)
            user = User(username=uname, password=pword)
            # Hashes the password
            user.hash_password(pword)
            # Adds to the database
            user.add(user)
            return ({'message': 'user created'}, 201)
        except exc.IntegrityError:
            return ({'message': 'user alredy exists'}, 400)

    def get(self):
        return({'message': 'Method is not allowed'}, 405)


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
                token = user.generate_token()
                return({'message': 'Login successful', 'token': token.decode('ascii')}, 200)
            else:
                return({'message': 'wrong username/password combination'}, 401)

    def get(self):
        return({'message': 'Method is not allowed'}, 405)


class BucketLists(Resource):
    @auth.login_required
    def get(self):
        pass

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Bucketname', required=True,
                            help="Bucket name cannot be blank")
        parser.add_argument('')


class BucketList(Resource):
    @auth.login_required
    def get(self, id):
        pass

    @auth.login_required
    def post(self, id):
        pass

    @auth.login_required
    def delete(self, id):
        pass


class BucketListItems(Resource):
    @auth.login_required
    def post(self, id):
        pass


class BucketListItem(Resource):
    @auth.login_required
    def put(self, id):
        pass

    @auth.login_required
    def delete(self, id):
        pass
