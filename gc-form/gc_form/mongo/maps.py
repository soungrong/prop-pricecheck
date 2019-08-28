import json
import os

import googlemaps
import pymongo

from gc_form.mongo.instance import db


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
    query = db.town.aggregate([
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
