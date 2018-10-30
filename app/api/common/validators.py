"""
File with all user input validation methods
"""
# Standard library import
import re
from functools import wraps

# Third party import
from flask import abort
from flask_jwt_extended import get_jwt_identity

# Local app imports
from app.api.v2.views.helpers import get_user_by_email


def common(expected_payload, json_data):
    """
    
    The expected payload is the expected data and we compare it 
    to the json data
    """
    for key in json_data.keys():
        if key not in expected_payload:
            msg = 'The field {} is not required'.format(key)
            return {"status":"Failed!","message":msg},400
    for item in expected_payload:
        if item not in json_data.keys():
            msg = 'Please provide the {} field'.format(item)
            return {"status":"Failed!","message":msg},400
    for item, value in json_data.items():
        if not isinstance(value, int):
            value_without_white_space = "".join(value.split())
            if value_without_white_space == "":
                msg = 'The {} can not be empty'.format(item)
                return {"status":"Failed!","message":msg},400



def commonp(json_data):
    """
    Function receives the input json data
    """
    for item, value in json_data.items():
        if item == 'name':
            if isinstance(value, int):
                msg = 'Name of the product can not be an integer'
                return {"status":"Failed!","message":msg},400
        if item == 'inventory' or item == 'price':
            if not isinstance(value, int):
                msg = 'Please make sure the {} is a number'.format(item)
                return {"status":"Failed!","message":msg},400

def valid_email(email):
    if not \
    re.match(r"^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$", email):
        msg = 'Please input a valid email'
        return {"status":"Failed!","message":msg},406


def new_store_validator(json_data):
    """
    A create new store user input validator
    """

    pay_load = ['name', 'category', 'email', 'password']
    res = common(pay_load, json_data)
    if not res:
        for item, value in json_data.items():
            if not isinstance(value, str):
                msg = 'The {} field is supposed to be a string'.format(item)
                res = {"status":"Failed!","message":msg},406
            if item == 'name' or \
                    item == 'category' or item == 'username':
                if len(value) <= 4:
                    msg = 'The {} must have atleast five characters'.format(item)
                    res = {"status":"Failed!","message":msg},406
            if item == 'password':
                if len(item) < 8:
                    msg = 'The {} must have atleast eight characters'
                    res= {"status":"Failed!","message":msg},406
            if item == 'email':
                res = valid_email(value)
    return res

def login_validator(json_data):
    expected_pay_load = ['email', 'password']
    res = common(expected_pay_load, json_data)
    return res


def product_validator(json_data):
    """
    A create new product user input validator
    """
    expected_pay_load = ['name', 'inventory', 'price']
    res = common(expected_pay_load, json_data)
    if not res:
        res = commonp(json_data)
    return res


def sales_validator(json_data):
    """
    Sales user input validator
    """

    pay_load = ['number']
    res = common(pay_load, json_data)
    if not res:
        for item in json_data.values():
            if not isinstance(item, int):
                msg = 'Number of products should be an int'
                res = {"status":"Failed!","message":msg},406
    return res


def category_validator(json_data):
    """
    Category user input validator
    """

    pay_load = ['name']
    common(pay_load, json_data)
    for item in json_data.values():
        if isinstance(item, int):
            msg = 'The category should be a string'
            return {"status":"Failed!","message":msg},406


def product_update_validator(json_data):
    """
    Product update user input validator
    """

    pay_load = ['name', 'inventory', 'price'] 
    def keycheck(expected_pay_load,give_pay_load):
        for item in give_pay_load.keys():
            if item not in expected_pay_load:
                msg = 'The field {} is not required'.format(item)
                return {"status":"Failed!","message":msg},400
    res = keycheck(pay_load,json_data)
    if not res:
        res = commonp(json_data)
    return res


def super_admin_required(f):
    """ A decorator for restricting certain routes to only superadmin/owner of the store"""
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user = get_user_by_email(get_jwt_identity())
        r = current_user[2]
        """
        The r : role
        """
        if r != 0:
            msg = "Only Super Admin can access these resource"
            return {"status":"Failed!","message":msg},406
        return f(*args, **kwargs)
    return decorator


def admin_required(f):
    """ A decorator for restricting certain routes to only admins"""
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user = get_user_by_email(get_jwt_identity())
        r = current_user[2]
        """
        The r : role
        """
        if r == 2 or r == 'Attendant':
            msg = "Only administrators can access these resource"
            return {"status":"Failed!","message":msg},406
        return f(*args, **kwargs)
    return decorator
    