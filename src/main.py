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
def get_users():
    try:
        users = [user.serialize() for user in User.query.all()]
        return jsonify(users)
    except:
        raise APIException('There are no users in the database', 404)

# get user favourites
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('No match')
    else:
        favourites = [item.serialize() for item in user.peopleFavourites + user.planetFavourites]
        return jsonify(favourites) 



#get all characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    try:
        response = [character.serialize() for character in Person.query.all()]
        return jsonify(response)
    except:
        raise APIException('There are no characters in the database', 404)

#get single character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
        response = Person.query.get(character_id)
        return jsonify(response.serialize())
    except:
        raise APIException('Character not found', 404)

# add favourite character
@app.route('/favourite/character/<int:character_id>', methods=['POST'])
def add_favourite_character(character_id):
    request_body = request.json.get("User")                     #expected request_body: {"User":{ "id": Integer}}
    user = User.query.get(request_body['id'])
    character = Person.query.get(character_id)

    if not user or not character:
        raise APIException('user or character not found')
    elif character in user.peopleFavourites:
        raise APIException('character already in favourites', 400)
    else:
        user.peopleFavourites.append(character)
        db.session.commit()
        return jsonify(f'{character} added', 200)

#delete favourite character
@app.route('/favourite/character/<int:character_id>', methods=['DELETE'])
def delete_favourite_character(character_id):
    request_body = request.json.get("User")                     #expected request_body: {"User":{ "id": Integer}}
    user = User.query.get(request_body['id'])
    character = Person.query.get(character_id)

    if not user or not character:
        raise APIException('user or person not found', 404)
    elif character not in user.peopleFavourites:
        raise APIException(f'{character} is not in favourites', 404)
    else:
        user.peopleFavourites.remove(character)
        db.session.commit()
        return jsonify(f'{character} removed from favourites', 200)



#get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
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

#add favourite planet
@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favourite(planet_id):
    request_body = request.json.get("User")                     #expected request_body: {"User":{ "id": Integer}}
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

#delete favourite planet
@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    request_body = request.json.get("User")                     #expected request_body: {"User":{ "id": Integer}}
    user = User.query.get(request_body['id'])
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        raise APIException('user or planet not found')
    elif planet not in user.planetFavourites:
        raise APIException('planet is not in favourites')
    else:
        user.planetFavourites.remove(planet)
        db.session.commit()
        return jsonify(f'{planet} removed from favourites')


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
