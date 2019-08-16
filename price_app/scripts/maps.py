import collections
import json
import os

import googlemaps
from pymongo import GEOSPHERE

from price_app.database import mongo


def geocode_towns(dataframe):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_KEY'))

    towns_names = dataframe.reset_index()['town'].unique()
    towns_geocoded = []

    for town in towns_names:
        request = gmaps.geocode(town, region='my')
        # this dict and array format is required by MongoDB
        geo_entry = {
                'location': {
                    'type': 'Point',
                    'coordinates': [
                        request[0]['geometry']['location']['lng'],
                        request[0]['geometry']['location']['lat']
                        ],
                    },
                'town': town,
        }
        towns_geocoded.append(geo_entry)

    return towns_geocoded


def save_to_json(towns_geocoded):
    with open('town_geo.json', 'w') as f:
        print(json.dumps(towns_geocoded), file=f)


def save_to_mongo(towns_geocoded):
    result = mongo.db.posts.insert_many(towns_geocoded)
    mongo.db.posts.create_index([("location", GEOSPHERE)])

    return result


def find_closest_points(lng, lat):
    query = mongo.db.posts.aggregate([{
        '$geoNear': {
            'near': {
                'type': 'Point',
                'coordinates': [ float(lng) , float(lat) ]
                },
            'distanceField': 'dist.calculated',
            'includeLocs': 'dist.location',
            'spherical': 'true',
            'limit': 3,
            }
        }])
    result = list(query)

    return result
