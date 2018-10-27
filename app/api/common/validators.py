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


def common(l, d):
    # receive a list and a dict
    # let list be l
    # let dict d
    for i in d.keys():
        if i not in l:
            msg = 'The field {} is not required'.format(i)
            return {"message":msg},400
    for i in l:
        if i not in d.keys():
            msg = 'Please provide the {} field'.format(i)
            return {"message":msg},400
    for i, v in d.items():
        if not isinstance(v, int):
            gv = "".join(v.split())
            if gv == "":
                msg = 'The {} can not be empty'.format(i)
                return {"message":msg},400
                #abort(400,msg)

def commonp(d):

    # let dict d
    for i, v in d.items():
        if i == 'name':
            if isinstance(v, int):
                msg = 'Name of the product can not be an integer'
                return {"message":msg},400
        if i == 'inventory' or i == 'price':
            if not isinstance(v, int):
                msg = 'Please make sure the {} is a number'.format(i)
                return {"message":msg},400

def new_store_validator(k):
    """
    A create new store user input validator
    """

    p_l = ['name', 'category', 'email', 'password']
    res = common(p_l, k)
    if not res:
        for i, v in k.items():
            if not isinstance(v, str):
                msg = 'The {} field is supposed to be a string'.format(i)
                res = {"message":msg},406
            if i == 'name' or \
                    i == 'category' or i == 'username':
                if len(v) <= 4:
                    msg = 'The {} must have atleast five characters'.format(i)
                    res = {"message":msg},406
            if i == 'password':
                if len(i) < 8:
                    msg = 'The {} must have atleast eight characters'
                    res= {"message":msg},406
            if i == 'email':
                if not \
                        re.match(r"^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$", v):
                    msg = 'Please input a valid email'
                    res = {"message":msg},406
    return res

def login_validator(k):
    p_l = ['email', 'password']
    res = common(p_l, k)
    return res


def product_validator(k):
    """
    A create new product user input validator
    """
    pay_load = ['name', 'inventory', 'price']
    res = common(pay_load, k)
    if not res:
        res = commonp(k)
    return res


def sales_validator(k):
    """
    Sales user input validator
    """

    pay_load = ['number']
    res = common(pay_load, k)
    if not res:
        for i in k.values():
            if not isinstance(i, int):
                msg = 'Number of products should be an int'
                res = {"message":msg},406
    return res


def category_validator(k):
    """
    Category user input validator
    """

    pay_load = ['name']
    common(pay_load, k)
    for i in k.values():
        if isinstance(i, int):
            msg = 'The category should be a string'
            return {"message":msg},406


def product_update_validator(k):
    """
    Product update user input validator
    """

    pay_load = ['name', 'inventory', 'price'] 
    def keycheck(pl,dict):
        for i in dict.keys():
            if i not in pl:
                msg = 'The field {} is not required'.format(i)
                return {"message":msg},400
    res = keycheck(pay_load,k)
    if not res:
        res = commonp(k)
    return res


def super_admin_required(f):
    """ A decorator for restricting certain routes to only superadmin/owner of the store"""
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user = get_user_by_email(get_jwt_identity())
        r = current_user[2]
        if r != 0:
            msg = "Only Super Admin can access these resource"
            return {"message":msg},406
        return f(*args, **kwargs)
    return decorator


def admin_required(f):
    """ A decorator for restricting certain routes to only admins"""
    @wraps(f)
    def decorator(*args, **kwargs):
        current_user = get_user_by_email(get_jwt_identity())
        r = current_user[2]
        if r == 2 or r == 'Attendant':
            msg = "Only administrators can access these resource"
            return {"message":msg},406
        return f(*args, **kwargs)
    return decorator
    