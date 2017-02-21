from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Config.config import configuration


db = SQLAlchemy()

from bucketlist.app import api_blue_print

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)
    db.init_app(app)
    app.register_blueprint(api_blue_print)

    return app

