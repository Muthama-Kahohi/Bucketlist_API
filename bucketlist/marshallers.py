from flask_restful import fields

# Module that maps records from the database into a json format that can be rendered in the api
BucketListItem_marshaller = {
    'id': fields.Integer,
    'item_name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
}

Bucketlist_marshaller = {
    'id': fields.Integer,
    'bucketlist_name': fields.String,
    'items': fields.Nested(BucketListItem_marshaller),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer
}

