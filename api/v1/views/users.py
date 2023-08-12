#!/usr/bin/python3
"""
Create api endpoints that handle all default RESTFul API actions:
GET, POST, PUT, DELETE
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """An api endpoint to retrieve all users objects using GET method"""
    users = [ur.to_dict() for ur in storage.all(User).values()]
    return jsonify(users)

@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """An api endpoint to retrieve the users objects by its id using
    GET method"""
    user = storage.get(User, user_id)

    """If users_id is not linked to any User object, raise a 404 error"""
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_users():
    """An api endpoint to add new users object to its existing objects"""
    """If data to post is not in json format or does not contain name
    attribute"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"})
    elif 'email' not in request.get_json():
        return jsonify({"error": "Missing email"})
    elif 'password' not in request.get_json():
        return jsonify({"error": "Missing password"})
    else:
        """Create new obj with the data and save in database"""
        post_data = request.get_json()
        obj_data = User(**post_data)
        obj_data.save()
        return (jsonify(obj_data.to_dict()), 201)

@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Api endpoint to update target users attributes in database"""
    """If HTTP body request is not a dictionary"""
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)

    target_user = storage.get(User, user_id)
    """If user with the id is not found"""
    if target_user is None:
        abort(404)
    ignore = ("id", "email", "created_at", "updated_at")
    """Convert HTTP body request to a dictionary"""
    data = request.get_json()
    for k in data.keys():
        if k in ignore:
            pass
        else:
            setattr(target_user, k, data[k])
    target_user.save()
    return jsonify(target_user.to_dict()), 200

@app_views.route("users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """An Api endpoint to delete target users from it's database"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return (jsonify({}), 200)
