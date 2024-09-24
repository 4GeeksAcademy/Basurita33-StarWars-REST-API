from flask import Flask, request, jsonify, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import User, Character, Planet, Vehicle, Favorite
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
    
    # Query favorites for current user
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    favorite_planets = [favorite.planet.serialize() for favorite in favorites if favorite.planet]
    favorite_characters = [favorite.character.serialize() for favorite in favorites if favorite.character]
    favorite_vehicles = [favorite.vehicle.serialize() for favorite in favorites if favorite.vehicle]
    
    return jsonify({
        "favorite_planets": favorite_planets,
        "favorite_characters": favorite_characters,
        "favorite_vehicles": favorite_vehicles
    }), 200


# POST a favorite planet for the current user
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    
    new_favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} added to favorites"}), 200

# POST a favorite character for the current user
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    user = User.query.get(CURRENT_USER_ID)
    character = Character.query.get(people_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    
    new_favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": f"Character {people_id} added to favorites"}), 200

# POST a favorite vehicle for the current user
@api.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user = User.query.get(CURRENT_USER_ID)
    vehicle = Vehicle.query.get(vehicle_id)
    if not user or not vehicle:
        return jsonify({"error": "User or Vehicle not found"}), 404

    new_favorite = Favorite(user_id=user.id, vehicle_id=vehicle.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} added to favorites"}), 200

# DELETE a favorite planet for the current user
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite Planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"Planet {planet_id} removed from favorites"}), 200

# DELETE a favorite character for the current user
@api.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    user = User.query.get(CURRENT_USER_ID)
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=character_id).first()
    if not favorite:
        return jsonify({"error": "Favorite Character not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"Character {character_id} removed from favorites"}), 200

# DELETE a favorite vehicle for the current user
@api.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def remove_favorite_vehicle(vehicle_id):
    user = User.query.get(CURRENT_USER_ID)
    favorite = Favorite.query.filter_by(user_id=user.id, vehicle_id=vehicle_id).first()
    if not favorite:
        return jsonify({"error": "Favorite Vehicle not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"Vehicle {vehicle_id} removed from favorites"}), 200

#GET Characters
@api.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    return jsonify({
        "message": "This is your GET characters request",
        "characters": [character.serialize() for character in characters]
    }), 200

#GET Planets
@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify({
        "message": "This is your GET planets request",
        "planets": [planet.serialize() for planet in planets]
    }), 200

#GET Vehicles
@api.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify({
        "message": "This is your GET vehicles request",
        "vehicles": [vehicle.serialize() for vehicle in vehicles]
    }), 200

#GET One Character
@api.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Character.query.get(people_id)
    
    if not character:
        return jsonify({"error": "Character not found"}), 404
    
    return jsonify({
        "message": "This is your GET character request",
        "character": character.serialize()
    }), 200

#GET One Planet
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify({
        "message": "This is your GET planet request",
        "planet": planet.serialize()
    }), 200

#GET One Vehicle
@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify({
        "message": "This is your GET vehicle request",
        "vehicle": vehicle.serialize()
    }), 200

#POST new Character
@api.route('/add_people', methods=['POST'])
def add_character():
    user = User.query.get(CURRENT_USER_ID)
    if not user or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can add characters."}), 403
    
    data = request.json
    new_character = Character(
        name=data['name'],
        birth_year=data.get('birth_year'),  # Use get() to handle optional fields
        gender=data.get('gender')
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"message": "Character added successfully"}), 201

#POST new Planet
@api.route('/add_planet', methods=['POST'])
def add_planet():
    user = User.query.get(CURRENT_USER_ID)
    if not user  or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can add planets."}), 403
    
    data = request.json
    new_planet = Planet(
        name=data['name'],
        population=data.get('population'),
        climate=data.get('climate')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"message": "Planet added successfully"}), 201

#POST new Vehicle
@api.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    user = User.query.get(CURRENT_USER_ID)
    if not user or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can add vehicles."}), 403
    
    data = request.json
    new_vehicle = Vehicle(
        name=data['name'],
        model=data.get('model'),
        vehicle_class=data.get('vehicle_class')
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle added successfully"}), 201

#DELETE Character
@api.route('/delete_people/<int:people_id>', methods=['DELETE'])
def delete_character(people_id):
    user = User.query.get(CURRENT_USER_ID)
    if not user or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can delete characters."}), 403
    
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    
    db.session.delete(character)
    db.session.commit()
    return jsonify("This is your DELETE character request"), 200

#DELETE Planet
@api.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    if not user or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can delete planets."}), 403
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    
    db.session.delete(planet)
    db.session.commit()
    return jsonify("This is your DELETE planet request"), 200

#DELETE Vehicle
@api.route('/delete_vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle():
    user = User.query.get(CURRENT_USER_ID)
    if not user or not user.is_admin:
        return jsonify({"error": "Acces denied. Only administrators can delete vehicles."}), 403
    
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify("This is your DELETE vehicle request"), 200