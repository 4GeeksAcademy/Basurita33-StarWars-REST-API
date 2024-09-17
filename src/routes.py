from flask import Flask, request, jsonify, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import User, Character, Planet, Vehicle
from utils import APIException
from app import db

api = Blueprint('api', __name__)

CURRENT_USER_ID = 1

# GET all users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200

# GET current user's favorites
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(CURRENT_USER_ID)
    if not user:
        return jsonify({"error": "User not found"}), 404
    favorites = {
        "favorite_planets": [planet.serialize() for planet in user.favorite_planets],
        "favorite_people": [character.serialize() for character in user.favorite_characters]
    }
    return jsonify(favorites), 200

# POST a favorite planet for the current user
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} added to favorites"}), 200

# POST a favorite character for the current user
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    user = User.query.get(CURRENT_USER_ID)
    character = Character.query.get(people_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    user.favorite_characters.append(character)
    db.session.commit()
    return jsonify({"message": f"Character {people_id} added to favorites"}), 200

# DELETE a favorite planet for the current user
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    if planet not in user.favorite_planets:
        return jsonify({"error": "Planet not in favorites"}), 400
    user.favorite_planets.remove(planet)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} removed from favorites"}), 200

# DELETE a favorite character for the current user
@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_character(people_id):
    user = User.query.get(CURRENT_USER_ID)
    character = Character.query.get(people_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    if character not in user.favorite_characters:
        return jsonify({"error": "Character not in favorites"}), 400
    user.favorite_characters.remove(character)
    db.session.commit()
    return jsonify({"message": f"Character {people_id} removed from favorites"}), 200

#GET Characters
@api.route('/people', methods=['GET'])
def get_people():
    return jsonify("This is your GET people request"), 200

#GET Planets
@api.route('/planets', methods=['GET'])
def get_planets():
    return jsonify("This is your GET planets request"), 200

#GET Vehicles
@api.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify("This is your GET vehicles request"), 200

#GET One Character
@api.route('/people/<int:people_id>', methods=['GET'])
def get_character():
    return jsonify("This is your GET character request"), 200

#GET One Planet
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet():
    return jsonify("This is your GET planet request"), 200

#GET One Vehicle
@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle():
    return jsonify("This is your GET vehicle request"), 200

#POST new Character
@api.route('/add_people', methods=['POST'])
def add_character():
    data = request.json
    new_character = Character(
        name=data['name'],
        birth_year=data['birth_year'],
        gender=data['gender']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"message": "Character added successfully"}), 201

#POST new Planet
@api.route('/add_planet', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(
        name=data['name'],
        population=data['population'],
        climate=data['climate']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"message": "Planet added successfully"}), 201

#POST new Vehicle
@api.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    new_vehicle = Vehicle(
        name=data['name'],
        model=data['model'],
        vehicle_class=data['vehicle_class']
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle added successfully"}), 201

#DELETE Character
@api.route('/delete_people/<int:people_id>', methods=['DELETE'])
def delete_character():
    return jsonify("This is your DELETE character request"), 200

#DELETE Planet
@api.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
def delete_planet():
    return jsonify("This is your DELETE planet request"), 200

#DELETE Vehicle
@api.route('/delete_vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle():
    return jsonify("This is your DELETE vehicle request"), 200