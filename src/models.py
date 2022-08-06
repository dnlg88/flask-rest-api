from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(8), unique=False, nullable=False)
    people = db.Column(db.List, unique=False)
    planets = db.Column(db.List, unique=False)
    favorite_person = relationship("FavoritePerson", lazy=True)
    favorite_planet = relationship("FavoritePlanet", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "people": self.people,
            "planets": self.planets
            # do not serialize the password, its a security breach
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    favorite_person = db.relationship('FavoritePerson', lazy=True)
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
    favorite_planet = db.relationship('FavoritePlanet', lazy=True)
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            # do not serialize the password, its a security breach
        }

class FavoritePlanet(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    name = db.Column(db.String(120), db.ForeignKey("Planet.name") ,unique=True, nullable=False)
    url = db.Column(db.String(80), db.ForeignKey("Planet.url"), unique=True, nullable=False)

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "url": self.url
            # do not serialize the password, its a security breach
        }

class FavoritePerson(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    name = db.Column(db.String(120), db.ForeignKey("Person.name") ,unique=True, nullable=False)
    url = db.Column(db.String(80), db.ForeignKey("Person.url"), unique=True, nullable=False)

    def __repr__(self):
        return '<FavoritePerson %r>' % self.name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "url": self.url
            # do not serialize the password, its a security breach
        }