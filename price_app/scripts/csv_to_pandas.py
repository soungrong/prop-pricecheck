from datetime import datetime

import pandas as pd
import pymongo
import numpy as np

from price_app.database import mongo


# limit display output to 2 decimal places
pd.options.display.float_format = '{:,.2f}'.format

pd.options.display.max_rows = 500


def process_csv(file_path, delimiter=',', quotechar='"'):
    dataframe = pd.read_csv(file_path, delimiter=delimiter, quotechar=quotechar)

    to_drop = ['city', 'state']
    dataframe.drop(columns=to_drop, inplace=True)

    dataframe.fillna(0, inplace=True)

    full_index = ['town', 'property_type', 'landed', 'rooms', 'plus_rooms',
        'bathrooms', 'car_parks', 'sub_type', 'floors', 'penthouse', 'soho',
        'studio', 'furnishing', 'position', 'price', 'size']

    pivot_source = pd.pivot_table(dataframe,
        values=['price','size'],
        index=full_index,
        aggfunc={
            'price': np.median,
            'size': np.median,
            },
        )

    index_criteria = ['town', 'property_type', 'landed', 'rooms', 'plus_rooms',
        'bathrooms', 'car_parks', 'sub_type', 'floors', 'penthouse', 'soho',
        'studio', 'furnishing', 'position']

    pivot_processed = pd.pivot_table(dataframe,
        values=['price','size'],
        index=index_criteria,
        aggfunc={
            'price': np.median,
            'size': np.median,
            },
        )

    # count how many records fit the index_criteria (this excludes price & size)
    pivot_processed['count'] = pivot_source.groupby(level=(0,1,2,3,4,5,6,7,8,9,10,11,12,13)).size()

    pivot_processed['price_per_sq_ft'] = pivot_processed['price'] / pivot_processed['size']

    rounded = pivot_processed.round(decimals=2)

    return rounded


def save_to_csv(dataframe):
    file_name = 'pandas-{}.csv'.format(
        datetime.now().strftime("%c").replace(' ', '-'))

    dataframe.to_csv(file_name)

    return file_name


def save_to_mongo(dataframe):
    # flatten rows/colums into individual dict records
    dataframe_dict = dataframe.reset_index().to_dict(orient='records')

    result = mongo.db.property.insert_many(dataframe_dict)
    mongo.db.property.create_index([("town", pymongo.ASCENDING)])

    return result
