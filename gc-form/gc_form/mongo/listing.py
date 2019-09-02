import pymongo

from .instance import Client


def closest_town_match(listing_query, closest_towns, user_sort_option="price"):
    """
    Iterates over all closest_town records, with given listing query until
    closest_town tuple is exhausted. Results are sorted by lowest price first on
    default. Returns None if no matches are found.
    """
    search_type = 'closest_town_match'
    search_iterations = 0
    mongo = Client()

    sort_option = (user_sort_option, pymongo.ASCENDING)

    sort_by = [
            ("rooms", pymongo.DESCENDING),
            ("plus_rooms", pymongo.DESCENDING),
            ("bathrooms", pymongo.DESCENDING),
            ("car_parks", pymongo.DESCENDING),
            ]

    sort_by.append(sort_option)

    for record in closest_towns:
        search_iterations += 1
        search_distance = record['distance']
        listing_query.update(town=record['town'])

        listings = mongo.db.listing.find(listing_query).limit(3).sort(sort_by)
        try:
            check_if_record_exists = listings[0]
            return (listings, search_type, search_iterations, search_distance)
        except IndexError:
            continue

    return (None,)


def closest_town_loose_match(listing_query, closest_towns, user_sort_option="price"):
    """
    Iterates over least_important_options, removing one criteria for each search
    attempt, until all least_important_options for all closest_towns are exhausted.
    Returns None if no matches are found.
    """
    search_type = 'closest_town_loose_match'
    search_iterations = 0
    mongo = Client()

    sort_option = (user_sort_option, pymongo.ASCENDING)

    sort_by = [
            ("rooms", pymongo.DESCENDING),
            ("plus_rooms", pymongo.DESCENDING),
            ("bathrooms", pymongo.DESCENDING),
            ("car_parks", pymongo.DESCENDING),
            ]

    sort_by.append(sort_option)

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
                listings = mongo.db.listing.find(loose_listing_query).limit(3).sort(sort_by)
                try:
                    check_if_record_exists = listings[0]
                    return (listings, search_type, search_iterations, search_distance)
                except IndexError:
                    continue

    return (None,)
