import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    TESTING = False
    ENV = 'development'

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "PLEASE CHANGE ME <3")  # TODO

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "app.db")

    LOGGING_DEFAULT_CONF = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s]-[%(levelname)-7s]-[%(module)s]:[%(funcName)s](%(lineno)d): %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }
