import os

# current directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # debug mode
    DEBUG = True
    # enable csrf
    CSRF_ENABLED = True
    # mini program's
    APP_ID = 'wx107f16d433135388'

    # folder maintains uploaded file
    UPLOAD_FOLDER = basedir + '/files/upload/'
    # folder maintains out file
    OUT_FOLDER = basedir + '/files/out/'
    # max size of uploaded file
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # commit on
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # track modifications is suggested opening
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # ...
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/zebra?charset=utf8mb4'


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/zebra?charset=utf8mb4'


configs = {
    'development': DevelopmentConfig,
    'product': ProductConfig
}
