import json

from app_server import create_app
from app_server.scripts import csv_to_pandas, towns
from gc_form.mongo.instance import db
from gc_form.mongo import maps, listing


# app = create_app()
# app.app_context().push()

# dataframe = csv_to_pandas.process_csv('app_server/data/cleaned-220819.csv')
# csv_to_pandas.save_to_mongo(dataframe)

# lat, lng = tb.reset_index().apply(append_geocode, axis=1, result_type="expand").T.values
# tb['lat'] = lat
# tb['lng'] = lng

# with open('app_server/data/town_geo.json') as json_file:
#     data = json.load(json_file)
#     towns.save_to_mongo(data)

# listing_query = {'rooms': {'$lte': 2}, 'plus_rooms': {'$lte': 1}, 'bathrooms': {'$lte': 2}, 'car_parks': {'$lte': 2}}

# b = maps.find_closest_towns(101.6278662, 3.1881946)

try:
    from IPython import embed
    # temporary color fix https://github.com/ipython/ipython/issues/11523
    embed(using=False)
except ImportError:
    import os
    import readline
    from pprint import pprint
    os.environ['PYTHONINSPECT'] = 'True'
