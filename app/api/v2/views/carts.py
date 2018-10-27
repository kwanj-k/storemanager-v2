"""
This file contains all the carts resources/endpoints
i.e get/delete/sell/update
"""


# Third party imports
from flask_restplus import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

# Local imports
from app.api.v2.models.cart import Cart
from app.api.v2.models.sale import Sale
from app.api.v2.db_config import cur
from app.api.v2.views.expect import CartEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email, get_store_id
from app.api.common.validators import sales_validator


add_to_cart = CartEtn.carts
v2 = CartEtn().v2


def cart_helper(email):
    """
    Method to get cart that belongs to a specific user
    """
    user = get_user_by_email(email)
    cur.execute("SELECT * FROM carts WHERE seller_id={};".format(user[0]))
    carts = cur.fetchall()
    return carts


@v2.route('')
class Carts(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    def get(self):
        """
        Get a cart
        """
        cart = cart_helper(get_jwt_identity())
        if not cart:
            return {"message":"You don\'t have any cart at the moment"},404
        all_cart_items = []
        totalamount = 0
        for c in cart:
            format_cart = {'entry_id': c[0],
                           'product': c[2],
                           'number_of_products': c[3],
                           'amount': c[4]}
            totalamount += c[4]
            all_cart_items.append(format_cart)
        return {"status": "Success!", "TotalAmount": totalamount,
                "Items": all_cart_items}, 200

    @v2.doc(security='apikey')
    @jwt_required
    def post(self):
        """
        Sell a cart
        """
        cart = cart_helper(get_jwt_identity())
        store_id = get_store_id(get_jwt_identity())
        if not cart:
            return {"message":"You don\'t have any cart at the moment"},404
        seller = get_user_by_email(get_jwt_identity())
        seller_id = seller[0]
        sale_order = []
        totalamount = 0
        for c in cart:
            product = c[2]
            number = c[3]
            amount = c[4]
            new_sale_record = Sale(
                store_id, seller_id, product, number, amount)
            new_sale_record.sell()
            format_sale = {'product': c[2],
                           'number_of_products': c[3],
                           'amount': c[4]}
            totalamount += c[4]
            sale_order.append(format_sale)
        cur.execute("DELETE FROM carts WHERE seller_id={};".format(seller_id))
        return {"status": "Sold!", "TotalAmount": totalamount,
                "Items": sale_order}, 201
    @v2.doc(security='apikey')
    @jwt_required
    def delete(self):
        """
        Delete an entire cart
        """
        cart = cart_helper(get_jwt_identity())
        if not cart:
            return {"message":"You don\'t have any cart at the moment"},404
        seller = get_user_by_email(get_jwt_identity())
        seller_id = seller[0]
        for c in cart:
            inventory = c[3]
            name = c[2]
            cur.execute(
                "UPDATE products SET inventory= inventory + '{}' WHERE name ='{}'".format(inventory, name))
        cur.execute("DELETE FROM carts WHERE seller_id={};".format(seller_id))
        return {"status": "Cart Deleted!"}, 200


@v2.route('/<int:id>')
class CartDetail(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    def put(self, id):
        """
        Update a product on a cart
        """
        json_data = request.get_json(force=True)
        res = sales_validator(json_data)
        if not res:
            cur.execute("SELECT * FROM carts WHERE id={};".format(id))
            product = cur.fetchone()
            seller = get_user_by_email(get_jwt_identity())
            seller_id = seller[0]
            if not product or product[1] != seller_id:
                return {"message":"That product is not in the cart"},404
            cur.execute(
                "SELECT * FROM products WHERE name='{}';".format(product[2]))
            p = cur.fetchone()
            number = json_data['number']
            if p[3] < int(number):
                msg = 'There are only {0} {1} available'.format(p[3], p[2])
                return {"message":msg},400
            new_amnt = number * p[4]
            cur.execute(
                "UPDATE carts SET number={0},amount={1} WHERE id ={2}".format(
                    number, new_amnt, id))
            conn.commit()
            new_p_inv = product[3] - int(number)
            cur.execute(
                "UPDATE products SET inventory= inventory + '{}' WHERE name ='{}'".format(
                    new_p_inv, product[2]))
            conn.commit()
            cur.execute("SELECT * FROM carts WHERE id={};".format(id))
            new_c = cur.fetchone()
            format_new_c = {
                "product": new_c[2],
                "number": new_c[3],
                "amount": new_c[4]
            }
            res = {"status": "Cart Updated", "cart": format_new_c}, 200
        return res
        
    @v2.doc(security='apikey')
    @jwt_required
    def delete(self, id):
        cur.execute("SELECT * FROM carts WHERE id={};".format(id))
        product = cur.fetchone()
        seller = get_user_by_email(get_jwt_identity())
        seller_id = seller[0]
        if not product or product[1] != seller_id:
            return {"message":"That product is not in the cart"},400
        new_p_inv = product[3]
        cur.execute(
            "UPDATE products SET inventory= inventory + '{}' WHERE name ='{}'".format(
                new_p_inv, product[2]))
        conn.commit()
        cur.execute("DELETE FROM carts WHERE id='{}';".format(id))
        format_c = {
            "product": product[2],
            "number": product[3],
            "amount": product[4]
        }
        return {"status": "Deleted!", "product": format_c}, 200
