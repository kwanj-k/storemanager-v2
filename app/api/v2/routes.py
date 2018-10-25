"""
This file contains all the routes
"""

# Third party imports
from flask import Blueprint
from flask_restplus import Api


# Local application imports
from .views.auth import v2 as newstore_route
from .views.auth import u2 as login_route

authorizations = {
    'apikey': {
       'type': 'apiKey',
       'in': 'header',
       'name': 'Authorization'
   }}

v_2 = Blueprint('v_2', __name__, url_prefix="/api/v2")
api = Api(v_2)
v2 = api.namespace(
    'v2',
    description='Store manager Api Using postgres',
    authorizations=authorizations)

api.add_namespace(newstore_route, path="/signup")
api.add_namespace(login_route, path="/")
