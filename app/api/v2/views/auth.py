"""
This file contains all the authentication resources/endpoints
i.e signup and login
"""


#Third party imports
from flask_restplus import Resource
from flask import request,abort
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity

#Local imports
from app.api.v2.models.accounts import Store,User
from app.api.v2.db_config import conn
from app.api.v2.views.expect import StoreEtn,UserEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email,get_store_by_name
from app.api.common.validators import login_validator,new_store_validator

#cursor to perform database operations
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
        json_data = request.get_json(force = True)
        new_store_validator(json_data)
        storecheck = get_store_by_name(json_data['name'])
        if storecheck:
            msg = 'Store name already exists'
            abort(406,msg)
        store_reg = Store(json_data['name'],
                            json_data['category'])
        store_reg.create_store()
        data = store_reg.json_dump()
        cur.execute("SELECT * FROM stores WHERE name='{}';".format(data['name']))
        store = cur.fetchone()
        store_id = store[0]
        role = 0
        usercheck = get_user_by_email(json_data['email'])
        if usercheck:
            msg = 'The user already exists'
            abort(406,msg)
        sup_ad_reg = User(store_id,role,
                        json_data['email'],
                        json_data ['password'])
        sup_ad_reg.create_user()
        user = sup_ad_reg.json_dump()
        res=  {"status":"Success!",
            "message":"Store successfully created","data":data,"user":user},201
        return res

@u2.route('auth/login')
class Login(Resource):
    @u2.expect(user_login)
    def post(self):
        """
        Login
        """
        json_data = request.get_json(force=True)
        user = get_user_by_email(json_data['email'])
        epass = json_data['password']
        if not user or not check_password_hash(user[4], epass):
            msg = 'Invalid credentials.If new,create a store first'
            abort(400, msg)
        access_token = create_access_token(identity=json_data['email'])
        return {"status": "Success!", "token": access_token}, 200