from price_app.database import db


class PropertyType(db.Model):
    __tablename__ = 'property_type'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    landed = db.Column('landed', db.Boolean, nullable=False)

    properties = db.relationship('Property', back_populates="property_type")


class Property(db.Model):
    __tablename__ = 'property'
    pk = db.Column(db.Integer, primary_key=True)
    price = db.Column('price', db.Integer, nullable=False)
    size = db.Column('size', db.Integer, nullable=False)
    position = db.Column('position', db.Enum('Intermediate', 'Corner', 'EndLot'))
    floors = db.Column('floors', db.Integer)
    rooms = db.Column('rooms', db.Integer, nullable=False)
    bathrooms = db.Column('bathrooms', db.Integer, nullable=False)
    plus_rooms = db.Column('plus_rooms', db.Integer)
    car_parks = db.Column('car_parks', db.Integer)
    studio = db.Column('studio', db.Boolean, default=False, nullable=False)
    soho = db.Column('soho', db.Boolean, default=False, nullable=False)
    penthouse = db.Column('penthouse', db.Boolean, default=False, nullable=False)
    furnishing = db.Column('sub_type', db.Enum('Unfurnished', 'Partly Furnished', 'Fully Furnished'))

    property_type_pk = db.Column('property_type', db.Integer, db.ForeignKey('property_type.pk'))
    state_pk = db.Column('state', db.Integer, db.ForeignKey('state.pk'))
    city_pk = db.Column('city', db.Integer, db.ForeignKey('city.pk'))


class State(db.Model):
    __tablename__ = 'state'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)

    cities = db.relationship('City', back_populates="state")
    properties = db.relationship('Property', back_populates="state")


class City(db.Model):
    __tablename__ = 'city'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)

    state = db.Column('state', db.Integer, db.ForeignKey('state.pk'))
    properties = db.relationship('Property', back_populates="city")
