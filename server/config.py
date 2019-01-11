"""
Project     : bugaboo
Filename    : config.py
Author      : zhancongc
Description : 配置文件
"""

import os

# current directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # debug mode
    DEBUG = True
    # enable csrf
    CSRF_ENABLED = True
    # csrf token
    SECRET_KEY = 'you will never guess'
    # mini program's
    APP_ID = 'wxc2de3e2ed4435707'
    # activity open
    APP_STATUS_ON = True
    # folder maintains uploaded file
    UPLOAD_FOLDER = basedir + '/app/static/compositions/'
    # folder maintains out file
    QRCODE_FOLDER = basedir + '/app/static/qrcode/'
    # domain url
    DOMAIN = 'https://bugaboo.drivetogreen.com'
    # image prefix
    COMPOSITION_PREFIX = DOMAIN + '/static/compositions/'
    # qrcode url prefix
    QRCODE_URL_PREFIX = '/receive/award/'
    # max size of uploaded file
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # migrate repository
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # time.strftime() format
    STRFTIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    # picture_allowed_extensions
    PICTURE_ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'gif', 'GIF', 'jpeg', 'JPEG'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/bugaboo_dev?charset=utf8mb4'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductConfig(Config):
    # database URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/bugaboo?charset=utf8mb4'
    # run log
    SQLALCHEMY_ECHO = True
    # log query
    SQLALCHEMY_RECORD_QUERIES = True
    # max connections
    SQLALCHEMY_MAX_OVERFLOW = 1000
    # connection timeout(second)
    SQLALCHEMY_POOL_RECYCLE = 600
    # modification track
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configs = {
    'development': DevelopmentConfig,
    'product': ProductConfig
}
