from flask_frozen import Freezer

from price_app import create_app


app = create_app()

# https://pythonhosted.org/Frozen-Flask/
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
