import collections
import json
import os

import googlemaps
import pymongo

from price_app.database import mongo


def geocode_towns(dataframe):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_KEY'))

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


def find_closest_points(lng, lat):
    query = mongo.db.town.aggregate([{
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
