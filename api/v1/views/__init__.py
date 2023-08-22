"""Create a blueprint instance so that other files can import from it"""
from flask import Blueprint

"""This url becomes the start of the access to all api endpoint"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""Import flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
