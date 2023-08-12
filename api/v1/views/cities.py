#!/usr/bin/python3
"""
Create api endpoints that handle all default RESTFul API actions:
GET, POST, PUT, DELETE
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_cities_in_state(state_id):
    """An api endpoint to retrieve the city objects in a state"""
    state = storage.get(State, state_id)

    """If state_id is not linked to any State object, raise a 404 error"""
    if state is None:
        abort(404)

    """turn each city to a dict and jsonify"""
    return jsonify([ct.to_dict() for ct in state.cities]), 200

@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_all_cities_by_id(city_id):
    """An api endpoint to retrieve city object by id"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return (jsonify(city.to_dict()), 200)

@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def post_city_by_state(state_id):
    """An api endpoint to add new city object to its existing objects"""
    """If data to post is not in json format or does not contain name
    attribute"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        """Create new obj with the data and save in database"""
        post_data = request.get_json()
        post_data['state_id'] = state.id
        obj_data = City(**post_data)
        obj_data.save()
        return (jsonify(obj_data.to_dict()), 201)

@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """An api endpoint to delete city object by its id"""
    cty = storage.get(City, city_id)
    if cty is None:
        abort(404)

    cty.delete()
    storage.save()
    return (jsonify({}), 200)

@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """An api endpoint to update the city object by its id"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    cty = storage.get(City, city_id)
    if cty is None:
        abort(404)
    new_name = request.get_json()
    cty.name = new_name['name']
    cty.save()
    return jsonify(cty.to_dict()), 200
