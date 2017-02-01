from flask_restful import fields

BucketListItem_marshaller = {
    'id': fields.Integer,
    'name': fields.String,
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
