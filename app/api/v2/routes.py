"""
This file contains all the routes
"""

# Third party imports
from flask import Blueprint
from flask_restplus import Api


# Local application imports
from .views.auth import v2 as newstore_route
from .views.auth import u2 as login_route
from .views.products import v2 as products_route
from .views.carts import v2 as cart_routes
from .views.categories import v2 as category_routes
from .views.sales import v2 as sales_routes

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
api.add_namespace(products_route, path="/products")
api.add_namespace(cart_routes, path="/cart")
api.add_namespace(category_routes, path="/categories")
api.add_namespace(sales_routes, path="/sales")
