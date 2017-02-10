from flask_restful import Resource, reqparse, marshal, request
from flask_httpauth import HTTPTokenAuth
from bucketlist.models import User, Bucketlist, BucketListItem
from bucketlist.__init__ import db
from sqlalchemy import exc
from flask import g
import datetime
from bucketlist.marshallers import *


auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    # Authenticating the token
    user = User.verify_authentication_token(token)
    if not user:
        return False
    g.user = user
    return True


class start(Resource):
    def get(self):
        return ({"message": "Welcome to my Api."}, 200)


class RegisterApi(Resource):
    '''Registers a new user'''

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
            user_name = credentials['username']
            pass_word = credentials['password']
            # Ensure that registration details are not blank
            if len(user_name) <= 0 or len(pass_word) <= 0:
                return({'message': 'please provide all credentials'}, 400)
            user = User(username=user_name, password=pass_word)
            # Hashes the password
            user.hash_password(pass_word)
            # Adds to the database
            user.add(user)
            return ({'message': 'user created'}, 201)
        except exc.IntegrityError:
            return ({'message': 'user alredy exists'}, 400)

    def get(self):
        '''Ensures that get method is not allowed for registration'''
        return({'message': 'Method is not allowed'}, 405)


class LoginApi(Resource):
    '''Logs in a user into the api. Give  the user a token to perfom transactions as authentication.'''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help="Username cannot be blank")
        parser.add_argument('password', required=True,
                            help="Password cannot be blank")
        credentials = parser.parse_args()
        user_name = credentials['username']
        pass_word = credentials['password']

        # confirm that the user does exist
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            return({'message': 'user does not exist'}, 404)
        else:
            # verify the password
            if user.veriry_password(pass_word, user.password):
                token = user.generate_token()
                return({'message': 'login successful',
                        'Authorization': token.decode('ascii')}, 200)
            else:
                return({'message': 'wrong username/password combination'}, 401)

    def get(self):
        '''Ensures that get method not allowed in logging in'''
        return({'message': 'Method is not allowed'}, 405)


class BucketLists(Resource):
    '''Adds and retrieves bucketlists to and from the database'''
    @auth.login_required
    def get(self):
        # Adds page and limit variables to be used for pagination
        page = request.args.get('page', 1)
        limit = request.args.get('limit', 20) or 100
        # Adds a query attribute specified in the url
        q = request.args.get('q')
        if q:
            # Searches bucketlists for one with the given query
            buckets = Bucketlist.query.filter(Bucketlist.bucketlist_name.ilike(
                '%' + q + "%")).filter_by(created_by=g.user.id).paginate(int(page), int(limit), False)
            bkts = buckets.items
            if buckets:
                if buckets.has_next:
                    next_page = str(
                        request.url_root) + 'bucketlist/api/bucketlists?q=' + q + '&page=' + str(int(page) + 1)
                else:
                    next_page = 'None'

                if buckets.has_prev:
                    prev = str(request.url_root) + 'bucketlist/api/bucketlists?q=' + \
                        q + '&page=' + str(int(page) - 1)
                else:
                    prev = 'None'
                buckets = [bucket for bucket in bkts]
                response = {'bucketlists': marshal(
                    buckets, Bucketlist_marshaller),
                    'next': next_page,
                    'prev': prev}
                return response, 200
            else:
                return {'message': ' Bucketlist not found'}, 404

        else:
            buckets = Bucketlist.query.filter_by(
                created_by=g.user.id).paginate(int(page), int(limit), False)
            bkts = buckets.items
            if buckets:
                if buckets.has_next:
                    next_page = str(
                        request.url_root) + \
                        'bucketlist/api/bucketlists?limit=' + str(int(limit)) + \
                        '&page=' + str(int(page) + 1)
                else:
                    next_page = 'None'

                if buckets.has_prev:
                    prev = str(request.url_root) + 'bucketlist/api/bucketlists?limit=' + \
                        str(int(limit)) + '&page=' + str(int(page) - 1)

                else:
                    prev = 'None'
                buckets = [bucket for bucket in bkts]
                response = {'bucketlists': marshal(
                    buckets, Bucketlist_marshaller),
                    'next': next_page,
                    'prev': prev}
                return response, 200

    @auth.login_required
    def post(self):
        '''
        Adds a new bucketlist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('Bucketname', required=True,
                            help="Bucket name cannot be blank")
        bucketlist = parser.parse_args()
        bucketname = bucketlist['Bucketname']
        # Ensures that bucketlist name is not empty
        if len(bucketname) > 0:
            bucket = Bucketlist.query.filter_by(
                bucketlist_name=bucketname).first()
            if bucket is not None:
                return({'message': 'Bucketlist already exists'}, 400)
            bucketlist = Bucketlist(bucketlist_name=bucketname,
                                    created_by=g.user.id)
            bucketlist.add(bucketlist)
            return({'message': 'Bucketlist successfully created'}, 201)
        else:
            return({'message': 'Bucketlist name cannot be blank'}, 400)


class BucketList(Resource):
    '''
    Retrievs specific bucketlist using an id
    '''
    @auth.login_required
    def get(self, id):
        bucketlists = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if bucketlists:
            return marshal(bucketlists, Bucketlist_marshaller), 200
        else:
            return ({'message': 'Bucketlist does not exist'}, 404)

    @auth.login_required
    def put(self, id):
        '''
        Updates a specific bucketlist using the id
        '''
        # Queries the db to ensure that search a bucketlist exists
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if bucketlist:
            parser = reqparse.RequestParser()
            parser.add_argument('Bucketname', required=True,
                                help="Username cannot be blank")
            update = parser.parse_args()
            bname = update['Bucketname']
            bucketlist.bucketlist_name = bname
            bucketlist.update()
            return({'message': 'Bucketlist Updated'}, 201)
        else:
            return({'message': 'Bucketlist does not exist'}, 404)

    @auth.login_required
    def delete(self, id):
        '''
        deletes specific bucketlist as per the id provided
        '''
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if bucketlist:
            bucketlist.delete(bucketlist)
            return ({'message': 'Bucketlist deleted'}, 200)
        else:
            return ({'message': 'Bucketlist does not exist'}, 404)


class BucketListItems(Resource):
    @auth.login_required
    def post(self, id):
        '''
        Adds a item to a bucketlist id given
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('item_name', required=True,
                            help='Item name cannot be blank')
        item_details = parser.parse_args()
        item_name = item_details['item_name']
        bucket = Bucketlist.query.filter_by(
            id=id).first()
        if bucket:
            if len(item_name) > 0:
                item = BucketListItem(item_name=item_name,
                                      bucketlist_name=id,
                                      done=False)

                item.add(item)
                return({'message': 'Bucket Item successfully added'}, 201)
            else:
                return({'message': 'Item name cannot be blank'}, 400)
        else:
            return({'message': 'No such bucketlist'}, 404)


class BucketItem(Resource):
    '''
    Updates a bucketlist item with item_id in bucketlist with id bucket_id
    '''

    @auth.login_required
    def put(self, bucket_id, item_id):
        parser = reqparse.RequestParser()
        parser.add_argument('item_name')
        parser.add_argument('done')

        itemdetails = parser.parse_args()
        item_name = itemdetails['item_name']
        done = itemdetails['done']
        bucket = Bucketlist.query.filter_by(
            id=bucket_id).first()
        if bucket:
            blist_item = BucketListItem.query.filter_by(
                id=item_id, bucketlist_name=bucket_id).first()
            # Filters what item details are to be updated
            if blist_item:
                if item_name and done:
                    blist_item.item_name = item_name
                    blist_item.done = done
                    blist_item.update()
                elif item_name and not done:
                    blist_item.item_name = item_name
                    blist_item.update()
                elif done and not item_name:
                    blist_item.done = done
                    blist_item.update()
                return({'message': 'Item successfully updated'}, 201)
            else:
                return({'message': 'No such item'}, 404)
        else:
            return({'message': 'No such bucketlist'}, 404)

    @auth.login_required
    def delete(self, bucket_id, item_id):
        '''
        Deletes bucketlist item with provided id
        '''
        blist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_name=bucket_id).first()
        if blist_item:
            blist_item.delete(blist_item)
            return ({'message': 'Item deleted'}, 200)
        else:
            return({'message': 'No such bucketlist'}, 404)
