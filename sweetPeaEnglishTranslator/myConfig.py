import os


class MyConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never_guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
