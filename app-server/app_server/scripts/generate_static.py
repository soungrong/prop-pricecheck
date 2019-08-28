from flask_frozen import Freezer

from app_server import create_app


app = create_app()

# https://pythonhosted.org/Frozen-Flask/
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
