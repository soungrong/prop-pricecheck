import os

from flask import Flask

from app_server.cli import csv_to_pandas_command
from app_server.local import bp


def create_app():
    app = Flask('app_server')

    _setup_cli(app)
    _register_blueprints(app)

    return app


def _setup_cli(app):
    app.cli.add_command(csv_to_pandas_command)


def _register_blueprints(app):
    app.register_blueprint(bp)
