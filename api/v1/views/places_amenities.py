#!/usr/bin/python3
'''
    RESTful API for class Review
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    '''
        return reviews by place, json form
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity_list = [r.to_dict() for r in place.amenities]
    return jsonify(amenity_list), 200

