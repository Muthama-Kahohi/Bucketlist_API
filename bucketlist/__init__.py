from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from Config.config import configuration
from flask_restful import Api

api_blue_print = Blueprint('api', __name__, url_prefix='/bucketlist/api')
# initialize the api class
api = Api(api_blue_print)

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)
    db.init_app(app)

    app.register_blueprint(api_blue_print)

    return app
