from bucketlist import create_app, db
from flask_restful import Api
from bucketlist.app import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app('default')
api = Api(app)
manager = Manager(app)
migrate = Migrate(app, db)
app_context = app.app_context()
app_context.push()
db.create_all()

api.add_resource(RegisterApi, '/bucketlist/api/auth/register')

api.add_resource(LoginApi, '/bucketlist/api/auth/login')

api.add_resource(BucketLists, '/bucketlist/api/bucketlists')
api.add_resource(
    BucketList, '/bucketlist/api/bucketlists/<int:id>')

api.add_resource(
    BucketListItems, '/bucketlist/api/bucketlists/<int:id>/items')

api.add_resource(
    BucketItem, '/bucketlist/api/bucketlists/<int:bucket_id>/items/<int:item_id>')

if __name__ == '__main__':
    app.run()
