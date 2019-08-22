import pymongo

from price_app.database import mongo


def closest_town_match(listing_query, closest_towns):
    """
    Iterates over all closest_town records, with given listing query until
    closest_town tuple is exhausted. Returns None if no matches are found.
    """
    search_type = 'closest_town_match'
    search_iterations = 0

    for record in closest_towns:
        search_iterations += 1
        search_distance = record['distance']
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
            return (listings, search_type, search_iterations, search_distance)
        except IndexError:
            continue

    return (None,)


def loose_criteria_match(listing_query, closest_towns):
    """
    Iterates over least_important_options, removing one criteria for each search
    attempt, until all least_important_options for all closest_towns are exhausted.
    Returns None if no matches are found.
    """
    search_type = 'loose_criteria_match'
    search_iterations = 0

    least_important_options = ('furnishing', 'position', 'floors', 'size',
        'property_type')

    for record in closest_towns:
        # copy listing_query values to loose_listing_query, so we can freely
        # mutate loose_listing_query
        loose_listing_query = listing_query
        search_distance = record['distance']
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
                    return (listings, search_type, search_iterations, search_distance)
                except IndexError:
                    continue

    return (None,)
