#!/usr/bin/python3
"""This contains functions to endpoint route to get the status of
my API
"""

"""Import storage and all classes"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def api_status():
    """Show api status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count_each_obj():
    """An endpoint that retrieves the number of each objects by type"""
    obj_counter = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(obj_counter)
