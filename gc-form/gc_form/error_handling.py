from google.cloud import error_reporting
from google.auth.exceptions import DefaultCredentialsError
import traceback


class ErrorHandler:
    """
    Wrapper for gcloud's Stackdriver logging, so exceptions are reported
    locally in dev environments if no credentials are present. Deployed
    gcloud functions automatically obtain credentials in their environment.
    """
    def __init__(self):
        try:
            self.client = error_reporting.Client()
        except DefaultCredentialsError:
            self.client = None

    def report_exception(self):
        if self.client is not None:
            self.client.report_exception()
        else:
            traceback.print_exc()
