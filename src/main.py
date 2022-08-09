"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all users
@app.route('/users', methods=['GET'])
def getUsers():
    try:
        users = [x.serialize() for x in User.query.all()]
        return jsonify(users)
    except:
        raise APIException('There are no users in the database', 404)

#get all characters
@app.route('/people', methods=['GET'])
def getPeople():
    try:
        response = [x.serialize() for x in Person.query.all()]
        return jsonify(response)
    except:
        raise APIException('There are no characters in the Database', 404)

#get single character
@app.route('/people/<int:person_id>', methods=['GET'])
def getPerson(person_id):
    try:
        response = Person.query.get(person_id)
        return jsonify(response.serialize())
    except:
        raise APIException('Character not found', 404)

#get all planets
@app.route('/planets', methods=['GET'])
def getPlanets():
    try:
        response = [x.serialize() for x in Planet.query.all()]
        return jsonify(response)
    except:
        raise APIException('There are no planets in the Database', 404)

#get single planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        response = Planet.query.get(planet_id)
        return jsonify(response.serialize())
    except:
        raise APIException('Planet not found', 404)

#add planet favourite
@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favourite(planet_id):
    request_body = request.json.get("User")
    user = User.query.get(request_body['id'])
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        raise APIException('user or planet not found')
    elif planet in user.planetFavourites:
        raise APIException('planet already in favourites', 400)
    else:
        user.planetFavourites.append(planet)
        db.session.commit()
        return jsonify(f'{planet} added', 200)

# add favourite character
@app.route('/favourite/people/<int:person_id>', methods=['POST'])
def add_person_favourite(person_id):
    request_body = request.json.get("User")                     #expected request_body: {"User":{ "id": X}}
    user = User.query.get(request_body['id'])
    person = Person.query.get(person_id)

    if not user or not person:
        raise APIException('user or character not found')
    elif person in user.peopleFavourites:
        raise APIException('character already in favourites', 400)
    else:
        user.peopleFavourites.append(person)
        db.session.commit()
        return jsonify(f'{person} added', 200)

#delete favourite planet
@app.route('/favourite/planet/<int:planet_id>')
def delete_favourite_planet(planet_id):
    request_body = request.json.get("User")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
