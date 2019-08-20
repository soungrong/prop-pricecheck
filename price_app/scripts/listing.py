from price_app.database import mongo

# select all records that match town.
# if records returned are == 1, then don't do any further filtering and just return that.

def find(town):
    return mongo.db.listing.find_one({
        'town': town,
    })
