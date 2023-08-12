#!/usr/bin/python3

"""
Register the blueprint app_views created in /views/__init__ to your
Flask instance app together with CORS
"""

from flask_cors import CORS
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv

""" Create a new app"""
app = Flask(__name__)

"""Allow cross origin resource sharing from this port and from all methods"""
CORS(app, origins="0.0.0.0")

"""Register the blueprint created in the folder __init__ file"""
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(self):
    """Close storage by closing query after each session"""
    storage.close()

@app.errorhandler(404)
def handle_err_404(err):
    """Rather than html file when resource is not found, return
    json format since it's a webservice or api
    """
    return make_response(jsonify({"error": 'Not found'}))


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
