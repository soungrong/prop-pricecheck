import json

from bson import json_util
from google.cloud import error_reporting
from google.auth.exceptions import DefaultCredentialsError

from price_app.scripts import maps, listing


try:
    gcloud_errors = error_reporting.Client()
except DefaultCredentialsError:
    pass


def process(request):
    global gcloud_errors

    # TODO validate/sanitize input
    form_data = request.form.to_dict().items()

    listing_query = dict()
    for key, value in form_data:
        if key != 'location' and key != 'geometry' and value != '':
            listing_query[key] = {
                '$lte': float(value)
                }
    try:
        geo_data = json.loads(request.form['geometry'])
        closest_towns = maps.find_closest_towns(geo_data['lng'], geo_data['lat'])

        result = listing.find(listing_query, closest_towns)
        return json_util.dumps(result[0])

    except BaseException:
        gcloud_errors.report_exception()
