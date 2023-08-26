#!/usr/bin/python3
"""
Create api endpoints that handle all default RESTFul API actions:
GET, POST, PUT, DELETE
"""
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    """An api endpoint to retrieve the place objects in a city"""
    city = storage.get(City, city_id)

    """If city_id is not linked to any City object, raise a 404 error"""
    if city is None:
        abort(404)

    """turn each place to a dict and jsonify"""
    return jsonify([pl.to_dict() for pl in city.places]), 200

@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_all_place_by_id(place_id):
    """An api endpoint to retrieve place object by id"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return (jsonify(place.to_dict()), 200)

@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """An api endpoint to add new place object to its existing objects"""
    """If data to post is not in json format or does not contain name
    attribute"""

    if not request.get_json():
        return jsonify({"error": "Not a JSON"})
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"})
    elif 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"})
    else:
        """Create new obj with the data and save in database"""
        post_data = request.get_json()
        city = storage.get(City, city_id)
        user = storage.get(User, post_data["user_id"])
        if city is None or user is None:
            abort(404)
        post_data['city_id'] = city.id
        post_data['user_id'] = user.id
        obj_data = Place(**post_data)
        obj_data.save()
        return (jsonify(obj_data.to_dict()), 201)

@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """An api endpoint to delete place object by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return (jsonify({}), 200)

@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """An api endpoint to update the place object by its id"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_name = request.get_json()
    place.name = new_name['name']
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_place():
    """retrieves all Place objects depending of the JSON in the
    body of the request"""

    """If the request is not in json format"""
    req = request.get_json()
    if not req:
        abort(404, "Not a JSON")

    """If the request is json but empty or does not have any of the key states,
    cities, and amenities, retrieve all Place objects"""
    if req is None or (
        req.get('states') is None and
        req.get('cities') is None and
        req.get('amenities') is None
        ):
        all_places = storage.all(Place)
        return jsonify([plc.to_dict() for plc in all_places.values()]), 200

    """If any of the optional keys are found, retrieve all its places"""
    place_obj = []
    
    """Get the array of state ids in the json value of the key states"""
    if req.get('states'):
        state_objs = []
        for ids in req.get('states'):
            state_objs.append(storage.get(State, ids))

        for st in state_objs:
            for cty in st.cities:
                for pl in cty.places:
                    place_obj.append(pl)

    """Get the array of city ids in the json value of the key cities"""
    if req.get('cities'):
        city_objs = []
        for ids in req.get('cities'):
            city_objs.append(storage.get(City, ids))

        for cty in city_objs:
            for pl in cty.places:
                """If place obj is not already in place_obj array"""
                if pl not in place_obj:
                    place_obj.append(pl)

    if req.get('amenities'):
        """If no state and cities key, use all place obj"""
        if not place_obj:
            place_obj = storage.all(Place).values()
        """Get all amenities obj in list"""
        amen_obj = [storage.get(Amenity, ids) for ids in req.get('amenities')]
        """Filter by adding only places with all the amenities specified"""
        place_obj = [plc for plc in place_obj if all(
            [ame in place.amenities for ame in amen_obj])]

    return jsonify([obj.to_dict() for obj in place_obj])

            
