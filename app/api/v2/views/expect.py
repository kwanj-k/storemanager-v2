"""
File contains the namespaces and
user input expectations
"""

#Third party import
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

