from price_app import create_app
from price_app.database import db
from price_app.models import PropertyType, Property, State, City, Town


app = create_app()
app.app_context().push()


try:
    from IPython import embed
    # temporary color fix https://github.com/ipython/ipython/issues/11523
    embed(using=False)
except ImportError:
    import os
    import readline
    from pprint import pprint
    os.environ['PYTHONINSPECT'] = 'True'
