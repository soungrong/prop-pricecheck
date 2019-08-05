from price_app.database import db


class PropertyType(db.Model):
    __tablename__ = 'property_type'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    landed = db.Column('landed', db.Boolean, nullable=False)

    properties = db.relationship('Property', backref="property_type")


class Property(db.Model):
    __tablename__ = 'property'
    pk = db.Column(db.Integer, primary_key=True)
    price = db.Column('price', db.Float(precision=2), nullable=False)
    size = db.Column('size', db.Float, nullable=False)
    position = db.Column('position', db.Enum(
        'Intermediate', 'Corner', 'EndLot', ''))
    sub_type = db.Column('sub_type', db.Enum('Duplex', 'Triplex', ''))
    floors = db.Column('floors', db.Float(precision=1))
    rooms = db.Column('rooms', db.Integer, nullable=False)
    bathrooms = db.Column('bathrooms', db.Integer, nullable=False)
    plus_rooms = db.Column('plus_rooms', db.Integer)
    car_parks = db.Column('car_parks', db.Integer)
    studio = db.Column('studio', db.Boolean, default=False, nullable=False)
    soho = db.Column('soho', db.Boolean, default=False, nullable=False)
    penthouse = db.Column('penthouse', db.Boolean,
                          default=False, nullable=False)
    furnishing = db.Column('furnishing', db.Enum(
        'Unfurnished', 'Partly Furnished', 'Fully Furnished'))

    property_type_pk = db.Column(db.Integer, db.ForeignKey('property_type.pk'))
    state_pk = db.Column(db.Integer, db.ForeignKey('state.pk'))
    city_pk = db.Column(db.Integer, db.ForeignKey('city.pk'))
    town_pk = db.Column(db.Integer, db.ForeignKey('town.pk'))


class State(db.Model):
    __tablename__ = 'state'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)

    cities = db.relationship('City', backref="state")
    properties = db.relationship('Property', backref="state")


class City(db.Model):
    __tablename__ = 'city'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)

    state_pk = db.Column(db.Integer, db.ForeignKey('state.pk'))
    towns = db.relationship('Town', backref="city")
    properties = db.relationship('Property', backref="city")


class Town(db.Model):
    __tablename__ = 'town'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)

    city_pk = db.Column(db.Integer, db.ForeignKey('city.pk'))
    properties = db.relationship('Property', backref="town")
