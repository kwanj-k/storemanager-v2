"""
This file contains all the sales resources/endpoints
i.e get all sales
"""


#Third party imports
from flask_restplus import Resource,Namespace
from flask import request,abort
from flask_jwt_extended import  get_jwt_identity,jwt_required

#Local imports
from app.api.v2.db_config import conn
from .helpers import get_user_by_email,get_store_id
from app.api.common.validators import admin_required

cur = conn.cursor()
v2 = Namespace('sales',description='Sale records')


@v2.route('')
class Sales(Resource):

    @v2.doc( security='apikey')
    @jwt_required
    @admin_required
    def get(self):
        """
        Get all sales
        """
        store_id = get_store_id(get_jwt_identity())
        cur.execute("SELECT * FROM sales WHERE store_id={};".format(store_id))
        sales = cur.fetchall()
        all_sales = []
        total_sales_worth = 0
        for s in sales:
            cur.execute("SELECT * FROM users WHERE id={};".format(s[2]))
            seller = cur.fetchone()
            seller_email = seller[3]
            format_s = {'product_name': s[3], 
                    'number_of_products': s[4], 
                    'Amount':  s[5],
                    'seller':seller_email,
                    'sold_on':s[6] }
            total_sales_worth += s[5]
            all_sales.append(format_s)
        return {"status":"Success!","Total_sales_worth":total_sales_worth,"sales":all_sales},200
