"""
File with all user input validation methods
"""
# Standard library import
import re

# Third party import
from flask import abort

# Local app imports
from app.api.v2.views.helpers import get_user_by_email

def common(l,d):
    #receive a list and a dict
    #let list be l
    #let dict d
    for i in d.keys():
        if i not in l:
            msg = 'The field {} is not required'.format(i)
            abort(400, msg)
    for i in l:
        if i not in d.keys():
            msg = 'Please provide the {} field'.format(i)
            abort(406, msg)
    for i,v in d.items():
        if not isinstance(v, int):
            gv = "".join(v.split())
            if gv == "":
                msg = 'The {} can not be empty'.format(i)
                abort(406, msg)


def new_store_validator(k):
    """
    A create new store user input validator
    """

    p_l = ['name', 'category', 'email', 'password']
    common(p_l,k)
    for i, v in k.items():
        if not isinstance(v, str):
            msg = 'The {} field is supposed to be a string'.format(i)
            abort(406, msg)
        if i == 'name' or \
                i == 'category' or i == 'username':
            if len(v) <= 4:
                msg = 'The {} must have atleast five characters'.format(i)
                abort(406, msg)
        if i == 'password':
            if len(i) < 8:
                msg = 'The {} must have atleast eight characters'
                abort(406, msg)
        if i == 'email':
            if not \
                    re.match(r"^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$", v):
                msg = 'Please input a valid email'
                abort(406, msg)

def login_validator(k):
    p_l = ['email', 'password']
    common(p_l,k)