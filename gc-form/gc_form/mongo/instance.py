import os

from pymongo import MongoClient


class Client:

    def __init__(self):
        self.MONGO_FULL_CONNECTION_URL = os.getenv('MONGO_FULL_CONNECTION_URL')
        self.MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
        self.MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
        self.MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'test')
        self.MONGO_CERT_PATH = os.getenv('MONGO_CERT_PATH')

        # with Scalingo, authentication fails when username and password is
        # passed as keyword arguments for some reason, so just use full URL
        # in production for now.
        if int(os.getenv('IS_MONGO_PRODUCTION', 0)):
            self.client = MongoClient(self.MONGO_FULL_CONNECTION_URL, tlsCAFile=self.MONGO_CERT_PATH)
        else:
            # local development connection
            self.client = MongoClient(
                host=self.MONGO_HOST,
                port=self.MONGO_PORT
            )

        self.db = self.client[self.MONGO_DATABASE]
