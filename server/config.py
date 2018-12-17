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
    # mini program's
    APP_ID = 'wxc2de3e2ed4435707'
    # application secret
    APPLICATION_SECRET = b'hard to guess'
    # folder maintains uploaded file
    UPLOAD_FOLDER = basedir + '/app/static/compositions/'
    # image prefix
    COMPOSITION_PREFIX = 'https://bugaboo.drivetogreen.com/static/compositions/'
    # folder maintains out file
    OUT_FOLDER = basedir + '/files/out/'
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
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/bugaboo?charset=utf8mb4'
    # 运行日志
    SQLALCHEMY_ECHO = True
    # 查询日志
    SQLALCHEMY_RECORD_QUERIES = True
    # 最大连接数
    SQLALCHEMY_MAX_OVERFLOW = 1000
    # 连接超时（秒）
    SQLALCHEMY_POOL_RECYCLE = 600
    # 修改记录追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configs = {
    'development': DevelopmentConfig,
    'product': ProductConfig
}
