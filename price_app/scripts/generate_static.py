from flask_frozen import Freezer

from price_app.local import app

# https://pythonhosted.org/Frozen-Flask/
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
