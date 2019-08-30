import os

from pymongo import MongoClient


MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_SSL = os.getenv('MONGO_SSL', 'false')
MONGO_REPLICA_SET = os.getenv('MONGO_REPLICA_SET')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'test')

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, ssl=MONGO_SSL,
    replicaset=MONGO_REPLICA_SET, username=MONGO_USERNAME,
    password=MONGO_PASSWORD)

db = client[MONGO_DATABASE]
