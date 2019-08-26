import collections
import json
import os

import googlemaps
import pymongo

from price_app.database import mongo


def geocode_towns(dataframe):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_KEY'))

    # create a list of unique town_names
    town_names = dataframe.reset_index()['town'].unique()
    town_geocoded = []

    for town in town_names:
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
        town_geocoded.append(geo_entry)

    return town_geocoded


def save_to_json(town_geocoded):
    with open('town_geo.json', 'w') as f:
        print(json.dumps(town_geocoded), file=f)


def save_to_mongo(town_geocoded):
    result = mongo.db.town.insert_many(town_geocoded)
    mongo.db.town.create_index([("location", pymongo.GEOSPHERE)])

    return result


def find_closest_towns(lng, lat, limit=None):

    query_args = {
        '$geoNear': {
            'near': {
                'type': 'Point',
                'coordinates': [ float(lng) , float(lat) ]
                },
            'distanceField': 'distance',
            'spherical': 'true',
            }
        }

    if limit is not None:
        query_args['$geoNear']['limit'] = limit

    # geoNear returns calculated distances in meters
    query = mongo.db.town.aggregate([
        query_args,
        {
        # do not include _id and location fields in returned records
        '$project': {
            "_id": 0,
            "location": 0,
        },
    }])
    result = tuple(query)

    return result
