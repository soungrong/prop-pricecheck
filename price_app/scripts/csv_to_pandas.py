from datetime import datetime

import pandas as pd
import numpy as np


# limit element output to 2 decimal places
pd.options.display.float_format = '{:,.2f}'.format

pd.options.display.max_rows = 500


def process_csv(file_path, delimiter=',', quotechar='"'):
    df = pd.read_csv(file_path, delimiter=delimiter, quotechar=quotechar)

    to_drop = ['city', 'state']
    df.drop(columns=to_drop, inplace=True)

    df.fillna(0, inplace=True)

    prop_index = ['town', 'property_type', 'landed', 'rooms', 'plus_rooms',
        'bathrooms', 'car_parks', 'sub_type', 'floors', 'penthouse', 'soho',
        'studio', 'furnishing', 'position', 'price', 'size']

    pivot = pd.pivot_table(df,
        values=['price','size'],
        index=prop_index,
        aggfunc={
            'price': np.median,
            'size': np.median,
            },
        )

    prop_index_2 = ['town', 'property_type', 'landed', 'rooms', 'plus_rooms',
        'bathrooms', 'car_parks', 'sub_type', 'floors', 'penthouse', 'soho',
        'studio', 'furnishing', 'position']

    pivot_2 = pd.pivot_table(df,
        values=['price','size'],
        index=prop_index_2,
        aggfunc={
            'price': np.median,
            'size': np.median,
            },
        )

    pivot_2['count'] = pivot.groupby(level=(0,1,2,3,4,5,6,7,8,9,10,11,12,13)).size()

    return pivot_2


def save_to_csv(dataframe):
    file_name = 'pandas-{}.csv'.format(
        datetime.now().strftime("%c").replace(' ', '-'))

    dataframe.to_csv(file_name)
    return file_name
