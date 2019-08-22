import pymongo

from price_app.database import mongo


def strict_find(listing_query, closest_towns):
    """
    Iterates over all closest_town records, with given listing query until
    closest_town tuple is exhausted. Returns None if no matches are found.
    """
    search_type = 'strict'
    search_iterations = 0

    for record in closest_towns:
        search_iterations += 1
        listing_query.update(town=record['town'])
        listings = mongo.db.listing.find(listing_query).limit(3).sort([
            ("rooms", pymongo.DESCENDING),
            ("plus_rooms", pymongo.DESCENDING),
            ("bathrooms", pymongo.DESCENDING),
            ("car_parks", pymongo.DESCENDING),
            ("price", pymongo.DESCENDING),
            ])
        try:
            check_if_record_exists = listings[0]
            return (listings, search_iterations, search_type)
        except IndexError:
            continue

    return (None, search_iterations, search_type)


def loose_find(listing_query, closest_towns):
    """
    Iterates over least_important_options, removing one criteria for each search
    attempt, until all least_important_options for all closest_towns are exhausted.
    Returns None if no matches are found.
    """
    search_type = 'loose'
    search_iterations = 0

    least_important_options = ('furnishing', 'position', 'floors', 'size',
        'property_type')

    for record in closest_towns:
        loose_listing_query = listing_query
        loose_listing_query.update(town=record['town'])

        for criteria in least_important_options:
            if loose_listing_query.pop(criteria, None) is not None:
                # attempt a search if criteria was loosened
                search_iterations += 1
                listings = mongo.db.listing.find(loose_listing_query).limit(3).sort([
                    ("rooms", pymongo.DESCENDING),
                    ("plus_rooms", pymongo.DESCENDING),
                    ("bathrooms", pymongo.DESCENDING),
                    ("car_parks", pymongo.DESCENDING),
                    ("price", pymongo.DESCENDING),
                    ])
                try:
                    check_if_record_exists = listings[0]
                    return (listings, search_iterations, search_type)
                except IndexError:
                    continue

    return (None, search_iterations, search_type)
