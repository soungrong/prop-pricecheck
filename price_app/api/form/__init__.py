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

    geo_data = json.loads(request.form['geometry'])
    query = dict()
    # TODO validate/sanitize input
    form_data = request.form.to_dict().items()
    for key, value in form_data:
        if key != 'location' and key != 'geometry' and value != '':
            query[key] = {
                '$lte': float(value)
                }
    try:
        closest_towns = maps.find_closest_towns(geo_data['lng'], geo_data['lat'])
        query['town'] = closest_towns[0]['town']

        result = listing.find(query)
        return json_util.dumps(result[0])

    except BaseException:
        gcloud_errors.report_exception()
