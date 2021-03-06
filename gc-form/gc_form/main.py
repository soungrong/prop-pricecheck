import json
import os

from bson import json_util
from flask import make_response
from voluptuous import Any, Coerce, Optional, Required, REMOVE_EXTRA, Schema


# this block handles the import nuances when deployed as a gcloud function
try:
    # non-relative import, since gc-form isn't installed as a package
    # when deployed as a gcloud function
    from mongo import maps, listing
    from error_handling import ErrorHandler
except ImportError:
    # relative import, when running the flask app-server in dev, since gc-form
    # is installed as a package there
    from .mongo import maps, listing
    from .error_handling import ErrorHandler


CORS_DOMAIN = os.getenv('CORS_DOMAIN')

error_handler = ErrorHandler()


def process_form(request):
    global error_handler

    try:
        # geometry form input is unvalidated
        geo_data = json.loads(request.form['geometry'])
        closest_towns = maps.find_closest_towns(geo_data['lng'], geo_data['lat'])

        # All Optional fields are set to '' if no input was given
        form_validator = Schema({
            Required('rooms'): Coerce(int),
            Required('plus_rooms'): Coerce(int),
            Required('bathrooms'): Coerce(int),
            Required('car_parks'): Coerce(int),
            Optional('property_type', default=''): str,
            Optional('size'): Any(Coerce(int), ''),
            Optional('floors'): Any(Coerce(int), ''),
            Optional('position'): Any(Coerce(float), ''),
            Optional('furnishing'): Any(Coerce(float), ''),
            Optional('user_sort_option', default='price'): str,
        }, extra=REMOVE_EXTRA)

        form_data = request.form.to_dict()
        validated_form = form_validator(form_data)

        # form the query arguments that will be passed to Mongo
        listing_query = dict()
        for key, value in validated_form.items():
            # property_type is a string value, so it's handled differently
            if key == 'property_type' and value != '':
                listing_query[key] = value
            elif key == 'user_sort_option' and value != '':
                user_sort_option = value
            elif value != '':
                listing_query[key] = {
                    # find entries that are less than or equals to value
                    # so there's a higher probability of finding at least one match
                    '$lte': value,
                    }

        search = listing.closest_town_match(listing_query, closest_towns, user_sort_option)
        if search[0] is None:
            search = listing.closest_town_loose_match(listing_query, closest_towns, user_sort_option)

        search_result, search_type, search_iterations, search_distance = search

        match = search_result[0].copy()
        match['search_type'] = search_type
        match['search_iterations'] = search_iterations
        match['search_distance'] = search_distance

        response = make_response(json_util.dumps(match), 200)
    except:
        error_handler.report_exception()
        response = make_response(json_util.dumps(match), 500)

    response.headers['Access-Control-Allow-Origin'] = CORS_DOMAIN
    return response
