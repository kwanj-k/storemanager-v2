"""
This file contains all the authentication resources/endpoints
i.e signup,login,addadmin and attendant
"""


# Third party imports
from flask_restplus import Resource
from flask import request, abort
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_mail import Message

# Local imports
from app.api.v2.models.accounts import Store, User
from app.apps import mail
from app.api.v2.db_config import conn
from app.api.v2.views.expect import StoreEtn, UserEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email, get_store_by_name
from app.api.common.validators import login_validator, new_store_validator, super_admin_required, admin_required

# cursor to perform database operations
cur = conn.cursor()


new_store = StoreEtn.stores
v2 = StoreEtn().v2

u2 = UserEtn().v2
user_login = UserEtn().users


@v2.route('')
class Stores(Resource):
    @v2.expect(new_store)
    def post(self):
        """
        Create a store
        """
        json_data = request.get_json(force=True)
        res = new_store_validator(json_data)
        if not res:
            storecheck = get_store_by_name(json_data['name'])
            if storecheck:
                return {"message":"Store name already exists"},409
            store_reg = Store(json_data['name'],
                            json_data['category'])
            store_reg.create_store()
            data = store_reg.json_dump()
            cur.execute(
                "SELECT * FROM stores WHERE name='{}';".format(data['name']))
            store = cur.fetchone()
            store_id = store[0]
            role = 0
            usercheck = get_user_by_email(json_data['email'])
            if usercheck:
                return {"message":"The user already exists"},409
            sup_ad_reg = User(store_id, role,
                            json_data['email'],
                            json_data['password'])
            sup_ad_reg.create_user()
            user = sup_ad_reg.json_dump()
            res = {"status": "Success!",
                "message": "Store successfully created", "data": data, "user": user}, 201
        return res


@u2.route('auth/login')
class Login(Resource):
    @u2.expect(user_login)
    def post(self):
        """
        Login
        """
        json_data = request.get_json(force=True)
        email = "".join(json_data['email'].split())
        password = "".join(json_data['password'].split())
        if email  == '':
            msg = 'The email field can not be empty'
            return {"message":msg},400
        if password=='':
            msg = 'The password field can not be empty'
            return {"message":msg},400
        user = get_user_by_email(email)
        if not user or not check_password_hash(user[4], password):
            return {"message":"Invalid credentials.If new,create a store first"},400
        access_token = create_access_token(identity=json_data['email'])
        return {"status": "Success!", "token": access_token}, 200


@u2.route('admin')
class AddAdmin(Resource):
    @u2.doc(security='apikey')
    @jwt_required
    @super_admin_required
    @u2.expect(user_login)
    def post(self):
        """
        Add Admin
        """
        json_data = request.get_json(force=True)
        res =login_validator(json_data)
        if not res:
            email = get_jwt_identity()
            newad = get_user_by_email(json_data['email'])
            if  newad and newad[2]<=1:
                return {"message":"User already exists and is Admin already"},409
            if newad and newad[2] == 2:
                cur.execute("DELETE FROM users WHERE email={};".format(json_data['email']))
                conn.commit()
            user = get_user_by_email(email)
            store_id = user[1]
            role = 1
            cur.execute(
                "SELECT * FROM stores WHERE id='{}';".format(store_id))
            store = cur.fetchone()
            store_name = store[1]
            user_reg = User(store_id,
                            role,
                            json_data['email'],
                            json_data['password'])
            user_reg.create_user()
            email = json_data['email']
            passd = json_data['password']
            msg = Message('{} new admin'.format(store_name), recipients = [email])
            body = 'You have been made admin at {} Store.\nUse the email < {} > and the password < {} > to login at the StoreMangerSite.'.format(store_name,email,passd)
            msg.body = body
            mail.send(msg)
            res = {"status": "Success!", "data": user_reg.json_dump()}, 201
        return res


@u2.route('attendant')
class AddAttendant(Resource):
    @u2.doc(security='apikey')
    @jwt_required
    @admin_required
    @u2.expect(user_login)
    def post(self):
        """
        Add Attendant
        """
        json_data = request.get_json(force=True)
        res = login_validator(json_data)
        if not res:
            newattendant = get_user_by_email(json_data['email'])
            if  newattendant and newattendant[2] == 2:
                return {"message":"User already exists and is an Attendant"},409
            if newattendant and newattendant[2] > 0:
                cur.execute("DELETE FROM users WHERE email={};".format(json_data['email']))
                conn.commit()
            email = get_jwt_identity()
            user = get_user_by_email(email)
            store_id = user[1]
            role = 2
            user_reg = User(store_id,
                            role,
                            json_data['email'],
                            json_data['password'])
            user_reg.create_user()
            cur.execute(
                "SELECT * FROM stores WHERE id='{}';".format(store_id))
            store = cur.fetchone()
            store_name = store[1]
            email = json_data['email']
            passd = json_data['password']
            msg = Message('{} new Attendant'.format(store_name), recipients = [email])
            body = 'You have been made Attendant at {} Store.\nUse the email < {} > and the password < {} > to login at the StoreMangerSite.'.format(store_name,email,passd)
            msg.body = body
            mail.send(msg)
            res = {"status": "Success!", "data": user_reg.json_dump()}, 201
        return res
