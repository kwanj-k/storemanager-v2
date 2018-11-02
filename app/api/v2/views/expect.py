"""
File contains the namespaces and
user input expectations
"""

# Third party import
from flask_restplus import fields, Namespace


class StoreEtn:
    """
    Store input data expectations
    """
    v2 = Namespace(
        'stores',
        description='Stores')
    stores = v2.model('Store', {
        'name': fields.String(required=True, description='The name of the store'),
        'category': fields.String(required=True, description='The category of the store'),
        'email': fields.String(required=True, description='The owners/stores email address'),
        'password': fields.String(required=True, description='The owners password')
    })


class UserEtn:
    """
    User login input data expectations
    """
    v2 = Namespace(
        'users',
        description='Users')
    users = v2.model('User', {
        'email': fields.String(required=True, description='The user\'s email address'),
        'password': fields.String(required=True, description='The user"s password')
    })


class EditPassEtn:
    v0 = Namespace(
        'Edit password',
        description='Change password')
    editpass = v0.model('User0', {
        'old_password': fields.String(required=True, description='The old user"s password'),
        'new_password': fields.String(required=True, description='The new user"s password')
    })


class DeleteUserEtn:
    v1 = Namespace(
        'Remove user',
        description='Revoke user\'s access ')
    deleteuser = v1.model('User1', {
        'email': fields.String(required=True, description='The user\'s email address')
    })


class ProductEtn:
    """
    Product input data expectations
    """
    v2 = Namespace(
        'products',
        description='Products related endpoints')
    products = v2.model('Product', {
        'name': fields.String(required=True, description='The name of the product'),
        'inventory': fields.Integer(required=True, description='The number of the given products'),
        'price': fields.Integer(required=True, description='The price of the product')
    })


class CartEtn:
    """
    Cart input data expectations
    """
    v2 = Namespace(
        'carts',
        description='carts')
    carts = v2.model('Cart', {
        'number': fields.Integer(required=True, description='The number of products to add')
    })


class CategoryEtn:
    """
    Category input data expectations
    """
    v2 = Namespace(
        'categories',
        description='Category related endpoints')
    categories = v2.model('Category', {
        'name': fields.String(required=True, description='The name of the category')
    })
