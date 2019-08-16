import collections
import json
import os

import googlemaps


def geocode_towns(dataframe):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_KEY'))

    town_list = dataframe.reset_index()['town'].unique()
    town_geocoded = collections.defaultdict(dict)

    for town in town_list:
        request = gmaps.geocode(town, region='my')
        # this dict and array format is required by MongoDB
        town_geocoded[town] = [
            request[0]['geometry']['location']['lng'],
            request[0]['geometry']['location']['lat']
            ]

    return town_geocoded


def save_to_json(geocode_dict):
    with open('town_geo.json', 'w') as f:
        print(json.dumps(geocode_dict), file=f)
