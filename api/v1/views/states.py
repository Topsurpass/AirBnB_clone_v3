#!/usr/bin/python3
"""
Create api endpoints that handle all default RESTFul API actions:
GET, POST, PUT, DELETE
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_state():
    """An api endpoint to retrieve all state objects using GET method"""
    states = [st.to_dict() for st in storage.all(State).values()]
    return jsonify(states)

@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """An api endpoint to retrieve the state objects by its id using
    GET method"""
    state = storage.get(State, state_id)

    """If state_id is not linked to any State object, raise a 404 error"""
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """An api endpoint to add new state object to its existing objects"""
    """If data to post is not in json format or does not contain name
    attribute"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"})
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"})
    else:
        """Create new obj with the data and save in database"""
        post_data = request.get_json()
        obj_data = State(**post_data)
        obj_data.save()
        return (jsonify(obj_data.to_dict()), 201)

@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Api endpoint to update target state attributes in database"""
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)

    target_state = storage.get(State, state_id)
    if target_state is None:
        abort(404)
    target_state.name = request.get_json()["name"]
    target_state.save()
    return (jsonify(target_state.to_dict()), 200)

@app_views.route("states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """An Api endpoint to delete target state from it's database"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return (jsonify({}), 200)
