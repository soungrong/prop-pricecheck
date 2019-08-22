import json

from bson import json_util
from google.cloud import error_reporting
from google.auth.exceptions import DefaultCredentialsError
from voluptuous import Any, Coerce, Optional, Required, REMOVE_EXTRA, Schema

from price_app.scripts import maps, listing


try:
    gcloud_errors = error_reporting.Client()
except DefaultCredentialsError:
    pass


def process(request):
    global gcloud_errors

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
    }, extra=REMOVE_EXTRA)

    form_data = request.form.to_dict()
    validated_form = form_validator(form_data)

    # form the query arguments that will be passed to Mongo
    listing_query = dict()
    for key, value in validated_form.items():
        if value != '':
            listing_query[key] = {
                # find entries that are less than or equals to value
                # so there's a higher probability of finding at least one match
                '$lte': value,
                }
    try:
        geo_data = json.loads(request.form['geometry'])
        closest_towns = maps.find_closest_towns(geo_data['lng'], geo_data['lat'])

        result = listing.find(listing_query, closest_towns)
        return json_util.dumps(result[0])

    except BaseException:
        gcloud_errors.report_exception()
