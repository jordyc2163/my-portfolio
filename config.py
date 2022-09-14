import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisisnotthekeytolookfor',
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'es', 'de', 'fr']
    POSTS_PER_PAGE = 3
