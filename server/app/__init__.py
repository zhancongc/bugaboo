from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import configs


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)
    return app


app = create_app('development')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

