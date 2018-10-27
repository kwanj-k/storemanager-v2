"""
This file contains all the products resources/endpoints
i.e get/post/put and delete products
this will contain an add to cart endpoint
"""


# Third party imports
from flask_restplus import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

# Local imports
from app.api.v2.models.product import Product
from app.api.v2.models.cart import Cart
from app.api.v2.db_config import cur
from app.api.v2.views.expect import ProductEtn, CartEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email, get_store_id
from app.api.common.validators import product_validator, sales_validator, product_update_validator, admin_required

new_product = ProductEtn().products
add_to_cart = CartEtn.carts
v2 = ProductEtn().v2


@v2.route('')
class Products(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    @v2.expect(new_product)
    def post(self):
        """
        Add a product to the manager
        """
        json_data = request.get_json(force=True)
        res = product_validator(json_data)
        if not res:
            store_id = get_store_id(get_jwt_identity())
            cur.execute(
                "SELECT * FROM products WHERE name='{}';".format(json_data['name']))
            product = cur.fetchone()
            if product and product[1] == store_id:
                msg = 'Product already exists.Update product inventory instead'
                return {"message":msg},409
            cat_name ='Category-not-set'
            new_pro = Product(store_id, json_data['name'],
                            json_data['inventory'],
                            json_data['price'],
                            cat_name)
            new_pro.add_product()
            res = new_pro.json_dump()
            res = {"status": "Success!",
                "message": "Product successfully added", "data": res}, 201
        return res




    @v2.doc(security='apikey')
    @jwt_required
    def get(self):
        """
        Get all products
        """
        store_id = get_store_id(get_jwt_identity())
        cur.execute(
            "SELECT * FROM products WHERE store_id={};".format(store_id))
        products = cur.fetchall()
        all_products = []
        for p in products:
            format_p = {'product_id': p[0],
                        'name': p[2],
                        'inventory': p[3],
                        'price': p[4],
                        'category': p[5],
                        'added_at': p[6]}
            all_products.append(format_p)
        if len(all_products) < 1:
            res= {"message":"There are no products at the moment"},404
            return res
        return {"status": "Success!", "products": all_products}, 200


@v2.route('/<int:id>')
class ProductDetail(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    def get(self, id):
        """
        Get single product
        """
        cur.execute("SELECT * FROM products WHERE id={};".format(id))
        product = cur.fetchone()
        store_id = get_store_id(get_jwt_identity())
        if not product or product[1] != store_id:
            msg = 'Product does not exist'
            return {"message":msg},404
        format_p = {
            "product_name": product[2],
            "inventory": product[3],
            "price": product[4],
            'category': product[5],
            'added_at': product[6]}
        return {"status": "Success!", "product": format_p}, 200

    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    @v2.expect(new_product)
    def put(self, id):
        """
        Update a product
        """
        json_data = request.get_json(force=True)
        res = product_update_validator(json_data)
        if not res:
            cur.execute("SELECT * FROM products WHERE id={};".format(id))
            product = cur.fetchone()
            store_id = get_store_id(get_jwt_identity())
            if not product or product[1] != store_id:
                return {"message": 'Product does not exist'}, 404
            name = product[2]
            inventory = product[3]
            price = product[4]
            if 'name' in json_data:
                name = json_data['name']
            if 'inventory' in json_data:
                inventory = json_data['inventory']
            if 'price' in json_data:
                price = json_data['price']
            cur.execute("UPDATE products SET name='{}',inventory='{}',price='{}'\
            WHERE id ={}".format(name, inventory, price, id))
            conn.commit()
            cur.execute("SELECT * FROM products WHERE id={};".format(id))
            new_p = cur.fetchone()
            format_new_p = {
                "product_name": new_p[2],
                "inventory": new_p[3],
                "price": new_p[4],
                'category': new_p[5],
                'added_at': new_p[6]
            }
            res = {"status": "Updated!", "product": format_new_p}, 200
        return res

    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    def delete(self, id):
        """
        Delete a product
        """
        cur.execute("SELECT * FROM products WHERE id={};".format(id))
        product = cur.fetchone()
        store_id = get_store_id(get_jwt_identity())
        if not product or product[1] != store_id:
            msg = 'Product does not exist'
            return {"message":msg},404
        cur.execute("DELETE FROM products WHERE id={};".format(id))
        conn.commit()
        format_p = {
            "product_name": product[2],
            "inventory": product[3],
            "price": product[4]
        }
        return {"status": "Deleted!", "pr0duct": format_p}, 200

    @v2.doc(security='apikey')
    @jwt_required
    @v2.expect(add_to_cart)
    def post(self, id):
        """
        Add a product to cart
        """
        json_data = request.get_json(force=True)
        res = sales_validator(json_data)
        if not res:
            number = json_data['number']
            cur.execute("SELECT * FROM products WHERE id={};".format(id))
            product = cur.fetchone()
            store_id = get_store_id(get_jwt_identity())
            if not product or product[1] != store_id:
                msg = 'Product does not exist'
                res= {"message":msg},404
            product_name = product[2]
            if product[3] < int(number):
                msg = 'There are only {0} {1} available '.format(
                    product[3], product_name)
                return {"message":msg},406
            amount = number * product[4]
            seller = get_user_by_email(get_jwt_identity())
            seller_id = seller[0]
            new_cart = Cart(seller_id, product_name, number, amount)
            new_cart.add_to_cart()
            res = new_cart.json_dump()
            new_inventory = product[3] - number
            cur.execute(
                "UPDATE products SET inventory={0} WHERE id ={1}".format(
                    new_inventory, id))
            res = {"status": "Added to cart", "product": res}
        return res
