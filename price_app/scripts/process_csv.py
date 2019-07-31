import csv

from price_app.database import db
from price_app.models import Property, PropertyType, State, City, Town


def process_csv(file_path, delimiter=',', quotechar='"'):
    with open(file_path, 'r') as file:

        data = csv.DictReader(file, delimiter=delimiter, quotechar=quotechar)

        coerce_int = ('price', 'rooms', 'plus_rooms', 'bathrooms',
                    'car_parks', 'landed', 'penthouse', 'levels', 'storeys',
                    'soho', 'studio', 'size')

        for row in data:
            for header in coerce_int:
                if header == 'levels':
                    row[header] = string_levels_to_int(row[header])
                elif (header == 'storeys' or header == 'price' or header == 'size') and row[header]:
                    row[header] = float(row[header])
                elif row[header]:
                    row[header] = int(row[header])
                # if value in field is blank, just set to zero
                else:
                    row[header] = 0
            process_item(**row, row=row)

def string_levels_to_int(string):
    return { 'Duplex': 1, 'Triplex': 2, '': 0 }[string]

def process_item(town, city, state, price, rooms, plus_rooms, bathrooms, car_parks,
        property_type, landed, position, penthouse, levels, storeys, soho, studio,
        size, furnishing, row=None):

    item_type, _ = get_one_or_create(
        PropertyType, name=property_type, landed=landed)

    item_state, _ = get_one_or_create(State, name=state)
    item_city, _ = get_one_or_create(City, name=city, state=item_state)
    item_town, _ = get_one_or_create(Town, name=town, city=item_city)

    item, _ = get_one_or_create(Property,
        price=price,
        size=size,
        position=position,
        floors=levels,
        rooms=rooms,
        bathrooms=bathrooms,
        plus_rooms=plus_rooms,
        car_parks=car_parks,
        studio=studio,
        soho=soho,
        penthouse=penthouse,
        furnishing=furnishing,
        property_type=item_type,
        state=item_state,
        city=item_city,
        town=item_town)

def get_one_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        print('Found {}'.format(instance))
        return instance, False
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        print('Created {}'.format(instance))
        return instance, True
