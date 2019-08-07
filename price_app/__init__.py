import os

from flask import Flask
from flask_migrate import Migrate

from price_app.cli import csv_to_sql_command, csv_to_pandas_command
from price_app.database import mongo, sql
from price_app.local import bp


def create_app():
    app = Flask('price_app')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["MONGO_URI"] = os.getenv('MONGO_DATABASE_URI')

    _instance_config(app)
    _setup_cli(app)
    _register_blueprints(app)
    _setup_sqlalchemy(app)
    _setup_mongo(app)

    return app


def _instance_config(app):
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def _setup_cli(app):
    app.cli.add_command(csv_to_sql_command)
    app.cli.add_command(csv_to_pandas_command)


def _register_blueprints(app):
    app.register_blueprint(bp)


def _setup_sqlalchemy(app):
    migrate = Migrate(app, sql)
    import price_app.models
    sql.init_app(app)


def _setup_mongo(app):
    mongo.init_app(app)
