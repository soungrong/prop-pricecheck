import pymongo

from price_app.database import mongo


# select all records that match town.
# if records returned are == 1, then don't do any further filtering and just return that.

def find(listing_query, closest_towns):

    # iterate over all closest_town records until at least one listing is found
    breakpoint()
    for record in closest_towns:
        try:
            listing_query.update(town=record['town'])
            listings = mongo.db.listing.find(listing_query).limit(3).sort([
                ("rooms", pymongo.DESCENDING),
                ("plus_rooms", pymongo.DESCENDING),
                ("bathrooms", pymongo.DESCENDING),
                ("car_parks", pymongo.DESCENDING),
                ("price", pymongo.DESCENDING),
                ])
            # IndexError is thrown here, if it fails
            at_least_one_record_exists = listings[0]
            break
        except IndexError:
            continue

    return listings
