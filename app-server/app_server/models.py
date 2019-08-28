from app_server.database import sql


class PropertyType(sql.Model):
    __tablename__ = 'property_type'
    pk = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column('name', sql.String, nullable=False)
    landed = sql.Column('landed', sql.Boolean, nullable=False)

    properties = sql.relationship('Property', backref="property_type")


class Property(sql.Model):
    __tablename__ = 'property'
    pk = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column('price', sql.Float(precision=2), nullable=False)
    size = sql.Column('size', sql.Float, nullable=False)
    position = sql.Column('position', sql.Enum(
        'Intermediate', 'Corner', 'EndLot', ''))
    sub_type = sql.Column('sub_type', sql.Enum('Duplex', 'Triplex', ''))
    floors = sql.Column('floors', sql.Float(precision=1))
    rooms = sql.Column('rooms', sql.Integer, nullable=False)
    bathrooms = sql.Column('bathrooms', sql.Integer, nullable=False)
    plus_rooms = sql.Column('plus_rooms', sql.Integer)
    car_parks = sql.Column('car_parks', sql.Integer)
    studio = sql.Column('studio', sql.Boolean, default=False, nullable=False)
    soho = sql.Column('soho', sql.Boolean, default=False, nullable=False)
    penthouse = sql.Column('penthouse', sql.Boolean,
                          default=False, nullable=False)
    furnishing = sql.Column('furnishing', sql.Enum(
        'Unfurnished', 'Partly Furnished', 'Fully Furnished'))

    property_type_pk = sql.Column(sql.Integer, sql.ForeignKey('property_type.pk'))
    state_pk = sql.Column(sql.Integer, sql.ForeignKey('state.pk'))
    city_pk = sql.Column(sql.Integer, sql.ForeignKey('city.pk'))
    town_pk = sql.Column(sql.Integer, sql.ForeignKey('town.pk'))


class State(sql.Model):
    __tablename__ = 'state'
    pk = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column('name', sql.String, nullable=False)

    cities = sql.relationship('City', backref="state")
    properties = sql.relationship('Property', backref="state")


class City(sql.Model):
    __tablename__ = 'city'
    pk = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column('name', sql.String, nullable=False)

    state_pk = sql.Column(sql.Integer, sql.ForeignKey('state.pk'))
    towns = sql.relationship('Town', backref="city")
    properties = sql.relationship('Property', backref="city")


class Town(sql.Model):
    __tablename__ = 'town'
    pk = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column('name', sql.String, nullable=False)

    city_pk = sql.Column(sql.Integer, sql.ForeignKey('city.pk'))
    properties = sql.relationship('Property', backref="town")
