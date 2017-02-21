from bucketlist import create_app, db
from bucketlist.app import *
from bucketlist.models import *

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.create_all()

if __name__ == '__main__':
    app.run()
