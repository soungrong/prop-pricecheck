from flask_frozen import Freezer

from app_server import create_app


def freeze():
    app = create_app()
    # https://pythonhosted.org/Frozen-Flask/
    freezer = Freezer(app)
    freezer.freeze()
