#!/usr/bin/python3
"""
Create api endpoints that handle all default RESTFul API actions:
GET, POST, PUT, DELETE
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """An api endpoint to retrieve all amenity objects using GET method"""
    amenity = [am.to_dict() for am in storage.all(Amenity).values()]
    return jsonify(amenity)

@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """An api endpoint to retrieve the amenity objects by its id using
    GET method"""
    amenity = storage.get(Amenity, amenity_id)

    """If state_id is not linked to any State object, raise a 404 error"""
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """An api endpoint to add new amenity object to its existing objects"""
    """If data to post is not in json format or does not contain name
    attribute"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"})
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"})
    else:
        """Create new obj with the data and save in database"""
        post_data = request.get_json()
        obj_data = Amenity(**post_data)
        obj_data.save()
        return (jsonify(obj_data.to_dict()), 201)

@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Api endpoint to update target amenity attributes in database"""
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)

    target_amenity = storage.get(Amenity, amenity_id)
    if target_amenity is None:
        abort(404)
    target_amenity.name = request.get_json()["name"]
    target_amenity.save()
    return (jsonify(target_amenity.to_dict()), 200)

@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """An Api endpoint to delete target state from it's database"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return (jsonify({}), 200)
