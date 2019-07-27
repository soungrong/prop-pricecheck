from importlib import import_module
import os

from flask import Flask
from flask_migrate import Migrate

from price_app.database import db
from price_app.local import bp


def create_app():
    app = Flask('price_app')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    _instance_config(app)
    _register_blueprints(app)
    _setup_db(app)

    return app


def _instance_config(app):
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def _register_blueprints(app):
    app.register_blueprint(bp)


def _setup_db(app):
    migrate = Migrate(app, db)
    import price_app.models
    db.init_app(app)
