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
        town_geocoded[town]['lat'] = request[0]['geometry']['location']['lat']
        town_geocoded[town]['lng'] = request[0]['geometry']['location']['lng']

    return town_geocoded


def save_to_json(geocode_dict):
    with open('town_geo.json', 'w') as f:
        print(json.dumps(geocode_dict), file=f)
