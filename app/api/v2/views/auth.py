"""
This file contains all the authentication resources/endpoints
i.e signup,login,addadmin and attendant
"""


# Third party imports
from flask_restplus import Resource
from flask import request, abort
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required,get_raw_jwt
from flask_mail import Message

# Local imports
from app.api.v2.models.accounts import Store, User
from app.apps import mail
from app.api.v2.db_config import conn
from app.api.v2.views.expect import StoreEtn, UserEtn,DeleteUserEtn,EditPassEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email, get_store_by_name
from app.api.common.validators import login_validator, new_store_validator, super_admin_required, admin_required,valid_email
from app.api.common.utils import logged_in_checker
# cursor to perform database operations
cur = conn.cursor()


new_store = StoreEtn.stores
v2 = StoreEtn().v2

u2 = UserEtn().v2
user_login = UserEtn().users
editpass = EditPassEtn.editpass
delete_user = DeleteUserEtn.deleteuser
e2 = EditPassEtn.v0
d2 = DeleteUserEtn.v1


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
            storecheck = get_store_by_name(json_data['name'].lower())
            if storecheck:
                return {"status":"Failed!", "message":"Store name already exists"},409
            store_name = json_data['name'].lower()
            store_reg = Store(store_name,
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
                return {"status":"Failed!","message":"The user already exists"},409
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
            return {"status":"Failed!","message":msg},400
        if password=='':
            msg = 'The password field can not be empty'
            return {"status":"Failed!","message":msg},400
        user = get_user_by_email(email)
        if not user or not check_password_hash(user[4], password):
            return {"status":"Failed!","message":"Invalid credentials.If new,create a store first"},400
        access_token = create_access_token(identity=json_data['email'])
        return {"status": "Success!", "token": access_token}, 200

@u2.route('auth/logout')
class Logout(Resource):
    @u2.doc(security='apikey')
    @jwt_required
    def post(self):
        """
        Logout
        """
        current_user = get_jwt_identity()
        if current_user is None:
            msg='Please login to access to access this resource'
            return {"status":"Failed!","message":msg},400
        jti = get_raw_jwt()['jti']
        b_token= """INSERT INTO
                tokens (token) VALUES ('{}')""" .format(jti)
        cur.execute(b_token)
        conn.commit()
        return {"status":"Success!","message": "Successfully logged out"}, 200

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
        current_user = get_jwt_identity()
        if current_user is None:
            msg='Please login to access to access this resource'
            return {"status":"Failed!","message":msg},400
        json_data = request.get_json(force=True)
        res =login_validator(json_data)
        if not res:
            email = get_jwt_identity()
            newad = get_user_by_email(json_data['email'])
            if  newad and newad[2]<=1:
                return {"status":"Failed!","message":"User already exists and is Admin already"},409
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
            res = {"status": "Success!","message":"Admin added!", "data": user_reg.json_dump()}, 201
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
        current_user = get_jwt_identity()
        if current_user is None:
            msg='Please login to access to access this resource'
            return {"status":"Failed!","message":msg},400
        json_data = request.get_json(force=True)
        res = login_validator(json_data)
        if not res:
            newattendant = get_user_by_email(json_data['email'])
            if  newattendant and newattendant[2] == 2:
                return {"status":"Failed!","message":"User already exists and is an Attendant"},409
            if newattendant and newattendant[2] > 0:
                cur.execute("DELETE FROM users WHERE email='{}';".format(json_data['email']))
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
            res = {"status": "Success!","message":"Attendant added!", "data": user_reg.json_dump()}, 201
        return res


@e2.route('editpassword')
class EditPassword(Resource):
    @e2.doc(security='apikey')
    @jwt_required
    @e2.expect(editpass)
    def put(self):
        """
        Edit password
        """
        current_user = get_jwt_identity()
        if current_user is None:
            msg='Please login to access to access this resource'
            return {"status":"Failed!","message":msg},400
        json_data = request.get_json(force=True)
        password = "".join(json_data['old_password'].split())
        email = get_jwt_identity()
        if password=='':
            msg = 'The password field can not be empty'
            return {"status":"Failed!","message":msg},400
        user = get_user_by_email(email)
        if  not check_password_hash(user[4], password):
            return {"status":"Failed!","message":"Invalid password."},400
        new_password = "".join(json_data['new_password'].split())
        hashed_pass = generate_password_hash(new_password)
        cur.execute(
                "UPDATE users SET password='{0}' WHERE email ='{1}';".format(
                    hashed_pass, email))
        conn.commit()
        return {"status":"success!","message":"Password Updated successifully"},200
        

@d2.route('user')
class DeleteUser(Resource):
    @d2.doc(security='apikey')
    @jwt_required
    @super_admin_required
    @d2.expect(delete_user)
    def delete(self):
        """
        Remove User
        """
        current_user = get_jwt_identity()
        if current_user is None:
            msg='Please login to access to access this resource'
            return {"status":"Failed!","message":msg},400
        json_data = request.get_json(force=True)
        email = "".join(json_data['email'].split())
        super_admin = get_jwt_identity()
        if super_admin==email:
            msg='The owner can not be deleted'
            return {"status":"Failed!","message":msg},406
        user = get_user_by_email(super_admin)
        store_id = user[1]
        del_user = get_user_by_email(email)
        if not del_user or del_user[1] != store_id:
            msg = 'User does not exist'
            return {"status":"Failed!","message":msg},404
        cur.execute("DELETE FROM users WHERE email='{}';".format(email))
        conn.commit()
        return {"status":"User deleted!"},200
        
        