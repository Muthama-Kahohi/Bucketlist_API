import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'y0UW1LLn3V3RkN0W'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'bucketlist.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
       'sqlite:///' + os.path.join(basedir, 'test_bucketlist.db')
    SECRET_KEY = 'ThI7BHDFJH1KJCD'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configuration = {
    'default': DevConfig,
    'testing': TestingConfig
}
