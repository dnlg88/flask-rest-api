from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            # do not serialize the password, its a security breach
        }

planetFavourites = db.Table('planetFavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

peopleFavourites = db.Table('peopleFavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), unique=False, nullable=False)
    peopleFavourites = db.relationship("Person", secondary=peopleFavourites, backref="users", lazy=True)
    planetFavourites = db.relationship("Planet", secondary=planetFavourites, backref="users", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.firstName

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.firstName,
            "last_name": self.lastName,
            "email": self.email
            # do not serialize the password, its a security breach
        }



# class FavoritePlanet(db.Model):
#     user_id = db.Column(db.Integer(), db.ForeignKey(User.id), primary_key=True)
#     name = db.Column(db.String(120), db.ForeignKey(Planet.name), unique=True, nullable=False)
#     url = db.Column(db.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         return '<FavoritePlanet %r>' % self.name

#     def serialize(self):
#         return {
#             "user_id": self.user_id,
#             "name": self.name,
#             "url": self.url
#             # do not serialize the password, its a security breach
#         }

# class FavoritePerson(db.Model):
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
#     name = db.Column(db.String(120), db.ForeignKey(Person.name), unique=True, nullable=False)
#     url = db.Column(db.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         return '<FavoritePerson %r>' % self.name

#     def serialize(self):
#         return {
#             "user_id": self.user_id,
#             "name": self.name,
#             "url": self.url
#             # do not serialize the password, its a security breach
#         }