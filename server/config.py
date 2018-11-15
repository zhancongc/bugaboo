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
    # ...
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/zebra?charset=utf8mb4'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductConfig(Config):
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/zebra?charset=utf8mb4'
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
