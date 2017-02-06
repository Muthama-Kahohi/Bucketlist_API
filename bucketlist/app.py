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
    print(user)
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
            return({'message': 'user does not exist'}, 404)
        else:
            # verify the password
            if user.veriry_password(pword, user.password):
                token = user.generate_token()
                return({'message': 'login successful',
                        'Authorization': token.decode('ascii')}, 200)
            else:
                return({'message': 'wrong username/password combination'}, 401)

    def get(self):
        return({'message': 'Method is not allowed'}, 405)


class BucketLists(Resource):
    @auth.login_required
    def get(self):
        page = request.args.get('page', 1)
        limit = request.args.get('limit', 1) or 100
        q = request.args.get('q')
        if q:
            buckets = Bucketlist.query.filter(Bucketlist.bucketlist_name.ilike(
                '%' + q + "%")).filter_by(created_by=g.user.id).paginate(int(page), int(limit), False)
            bkts = buckets.items
            if buckets:
                if buckets.has_next:
                    next_page = str(
                        request.url_root) + 'bucketlist/api/bucketlist?q=' + str(q) + '&page=' + str(page + 1)
                else:
                    next_page = 'None'

                if buckets.has_prev:
                    prev = str(request.url_root) + 'bucketlist/api/bucketlists?q=' + \
                        str(q) + '&page=' + str(page - 1)
                else:
                    prev = 'None'
                buckets = [bucket for bucket in bkts]
                response = {'bucketlists': marshal(
                    buckets, Bucketlist_marshaller),
                    'next': next_page,
                    'prev': prev}
                return response
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
                        'bucketlist/api/bucketlist?limit=' + str(limit) + \
                        '&page=' + str(page + 1)
                else:
                    next_page = 'None'

                if buckets.has_prev:
                    prev = str(request.url_root) + 'bucketlist/api/bucketlist?limit=' + \
                        str(limit) + '&page=' + str(page - 1)

                else:
                    prev = 'None'
                buckets = [bucket for bucket in bkts]
                response = {'bucketlists': marshal(
                    buckets, Bucketlist_marshaller),
                    'next': next_page,
                    'prev': prev}
                return response
        bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
        return (marshal(bucketlists, Bucketlist_marshaller), 200)

    @auth.login_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('Bucketname', required=True,
                            help="Bucket name cannot be blank")
        bucketlist = parser.parse_args()
        bucketname = bucketlist['Bucketname']
        if len(bucketname) > 0:
            bucket = Bucketlist.query.filter_by(
                bucketlist_name=bucketname).first()
            if bucket is not None:
                return({'message': 'Bucketlist already exists'}, 400)
            bucketlist = Bucketlist(bucketlist_name=bucketname,
                                    date_created=datetime.datetime.now(),
                                    date_modified=datetime.datetime.now(),
                                    created_by=g.user.id)
            bucketlist.add(bucketlist)
            return({'message': 'Bucketlist successfully created'}, 201)
        else:
            return({'message': 'Bucketlist name cannot be blank'}, 400)


class BucketList(Resource):
    @auth.login_required
    def get(self, id):
        bucketlists = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if bucketlists:
            return marshal(bucketlists, Bucketlist_marshaller)
        else:
            return ({'message': 'Bucketlist does not exist'}, 404)

    @auth.login_required
    def put(self, id):
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
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if bucketlist:
            bucketlist.delete(bucketlist)
            return ({'message': 'Bucketlist deleted'})
        else:
            return ({'message': 'Bucketlist does not exist'}, 404)


class BucketListItems(Resource):
    @auth.login_required
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('item_name', required=True,
                            help='Item name cannot be blank')

        item_details = parser.parse_args()
        item_name = item_details['item_name']
        if len(item_name) > 0:
            item = BucketListItem(item_name=item_name,
                                  bucketlist_name=id,
                                  date_created=datetime.datetime.now(),
                                  date_modified=datetime.datetime.now(),
                                  done=False)

            item.add(item)
            return({'message': 'Bucket Item successfully added'}, 201)
        else:
            return({'message': 'Item name cannot be blank'})


class BucketItem(Resource):
    @auth.login_required
    def put(self, bucket_id, item_id):
        print(bucket_id, item_id)
        parser = reqparse.RequestParser()
        parser.add_argument('item_name')
        parser.add_argument('done')

        itemdetails = parser.parse_args()
        item_name = itemdetails['item_name']
        done = itemdetails['done']

        blist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_name=bucket_id).first()
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
            return({'message': 'Item successfully updated'})
        else:
            return({'message': 'No such item'})

    @auth.login_required
    def delete(self, bucket_id, item_id):
        blist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_name=bucket_id).first()
        if blist_item:
            blist_item.delete(blist_item)
            return ({'message': 'Item deleted'})
        else:
            return({'message': 'No such bucketlist'})
