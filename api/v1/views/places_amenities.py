#!/usr/bin/python3
'''
    RESTful API for class Review
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    '''
        return reviews by place, json form
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_list = [a.to_dict() for a in place.amenities]
    else:
        amenity_list = [storage.get(Amenity, a).to_dict() for a in place.amenity_ids]
    return jsonify(amenity_list), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False)
def del_amenity(place_id, amenity_id):
    """Delete amenity by its id from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
        
    for pl_amen in place.amenities:
        if pl_amen.id == amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Link amenity(s) to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        """If the Amenity is already linked to the Place, return the
        Amenity with the status code 200"""
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        """used amenity_id because amenity_ids is an array of ids(string)"""
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
