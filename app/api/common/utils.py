"""
A utilities file
A place for reuseable code
"""
# standard library import
from datetime import datetime


# Third party import
from flask_jwt_extended import get_jwt_identity

d1 = datetime.now()
d = d1.strftime('%H:%M%P %A %d %B %Y')


def myconverter(o):
    return o.__str__()


dt = myconverter(d)


def logged_in_checker():
    current_user = get_jwt_identity()
    if current_user is None:
        msg = 'Please login to access to access this resource'
        return {"status": "Failed!", "message": msg}, 400
