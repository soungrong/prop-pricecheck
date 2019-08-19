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

    try:
        points = maps.find_closest_points(geo_data['lng'], geo_data['lat'])
        query = {
            'town': points[0]['town'],
        }
        result = listing.find(**query)
        return json_util.dumps(result)
    except BaseException:
        gcloud_errors.report_exception()
