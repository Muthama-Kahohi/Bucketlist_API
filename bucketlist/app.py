from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class RegisterApi(Resource):

    def post(self, username, password):
        pass


class LoginApi(Resource):

    def post(self, username, password):
        pass


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


api.add_resource(RegisterApi, 'bucketlist/api/v1.0/auth/register',
                 endpoint='auth')

api.add_resource(LoginApi, 'bucketlist/api/v1.0/auth/login', endpoint='auth')

api.add_resource(BucketLists, 'bucketlist/api/v1.0/bucketlists',
                 endpoint='bucketlists')
api.add_resource(
    BucketList, 'bucketlist/api/v1.0/bucketlists/<int:id>', endpoint='bucketlists')

app.add_resource(
    BucketListItems, 'bucketlist/api/v1.0/bucketlists/<int:id>/items', endpoint='items')

app.add_resource(
    BucketListItem, 'bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', endpoint='items')
