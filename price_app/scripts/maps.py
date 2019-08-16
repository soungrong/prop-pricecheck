import collections
import json
import os

import googlemaps


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


def save_to_json(geocode_dict):
    with open('town_geo.json', 'w') as f:
        print(json.dumps(geocode_dict), file=f)
