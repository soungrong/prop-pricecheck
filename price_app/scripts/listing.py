import pymongo

from price_app.database import mongo


# select all records that match town.
# if records returned are == 1, then don't do any further filtering and just return that.

def find(query):
    result = mongo.db.listing.find(query).limit(3).sort([
        ("rooms", pymongo.DESCENDING),
        ("plus_rooms", pymongo.DESCENDING),
        ("bathrooms", pymongo.DESCENDING),
        ("car_parks", pymongo.DESCENDING),
        ("price", pymongo.DESCENDING),
        ])
    return result
