from google.cloud import error_reporting
from google.auth.exceptions import DefaultCredentialsError


try:
    gcloud_errors = error_reporting.Client()
except DefaultCredentialsError:
    pass


def process_form(request):
    global gcloud_errors

    try:
        return 'processed the post request.'
    except BaseException:
        gcloud_errors.report_exception()
