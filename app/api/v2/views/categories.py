"""
This file contains all the categories resources/endpoints
i.e get/put/delete/post and a category to product
"""


# Third party imports
from flask_restplus import Resource
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

# Local imports
from app.api.v2.models.category import Category
from app.api.v2.models.product import Product
from app.api.v2.db_config import cur
from app.api.v2.views.expect import CategoryEtn,ProductEtn
from app.api.v2.db_config import conn
from .helpers import get_user_by_email, get_store_id
from app.api.common.validators import category_validator, admin_required,product_validator

new_cat = CategoryEtn().categories
v2 = CategoryEtn.v2
new_product = ProductEtn().products

@v2.route('')
class Categories(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    @v2.expect(new_cat)
    def post(self):
        """
        Create a category
        """
        json_data = request.get_json(force=True)
        category_validator(json_data)
        store_id = get_store_id(get_jwt_identity())
        cur.execute(
            "SELECT * FROM categories WHERE name='{}';".format(json_data['name']))
        category = cur.fetchone()
        if category and category[1] == store_id:
            return {"message":"Category already exists"},409
        name = json_data['name']
        new_cat = Category(store_id, name)
        new_cat.add_category()
        return {"status": "Success!", "Category": new_cat.json_dump()}, 201

    @v2.doc(security='apikey')
    @jwt_required
    def get(self):
        """
        Get all get categories
        """
        store_id = get_store_id(get_jwt_identity())
        cur.execute(
            "SELECT * FROM categories WHERE store_id='{}';".format(store_id))
        categories = cur.fetchall()
        if len(categories) < 1:
            return {"message":"There are no categories at this time"},404
        all_categories = []
        for c in categories:
            format_cat = {
                "id": c[0],
                "name": c[2],
                "Added_at": c[3]
            }
            all_categories.append(format_cat)
        return {"status": "Success!", "categories": all_categories}, 200


@v2.route('/<int:id>')
class CategoryDetail(Resource):
    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    @v2.expect(new_cat)
    def put(self, id):
        """
        Update a category
        """
        json_data = request.get_json(force=True)
        category_validator(json_data)
        cur.execute("SELECT * FROM categories WHERE id={};".format(id))
        category = cur.fetchone()
        store_id = get_store_id(get_jwt_identity())
        if not category or category[1] != store_id:
            msg = {"message": 'Category does not exist'}, 404
            return msg
        name = category[2]
        cur.execute(
            "UPDATE categories SET name='{}' WHERE id ={}".format(
                name, id))
        conn.commit()
        cur.execute("SELECT * FROM categories WHERE id={};".format(id))
        new_c = cur.fetchone()
        format_new_c = {
            "category_name": new_c[2]
        }
        return {"status": "Updated!", "category": format_new_c}, 200

    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    def delete(self, id):
        cur.execute("SELECT * FROM categories WHERE id={};".format(id))
        category = cur.fetchone()
        store_id = get_store_id(get_jwt_identity())
        if not category or category[1] != store_id:
            msg = {"message": 'Category does not exist'}, 404
            return msg
        cur.execute("DELETE FROM  categories WHERE id={};".format(id))
        conn.commit()
        format_c = {
            "category_name": category[2]
        }
        return {"status": "Deleted!", "prpduct": format_c}, 200


@v2.route('/<int:id>/products')
class ProductCategory(Resource):

    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    @v2.expect(new_product)
    def post(self,id):
        """
        Add a new product to a category
        """
        store_id = get_store_id(get_jwt_identity())
        cur.execute("SELECT * FROM categories WHERE id='{}';".format(id))
        category = cur.fetchone()
        if not category or category[1] != store_id:
            msg = 'Category does not exist'
            return {"message":msg},404
        json_data = request.get_json(force=True)
        product_validator(json_data)
        cur.execute(
            "SELECT * FROM products WHERE name='{}';".format(json_data['name']))
        product = cur.fetchone()
        if product and product[1] == store_id:
            msg = 'Product already exists.Update product inventory instead'
            return {"message":msg},409
        cat_name = category[2]
        new_pro = Product(store_id, json_data['name'],
                          json_data['inventory'],
                          json_data['price'],
                          cat_name)
        new_pro.add_product()
        res = new_pro.json_dump()
        res = {"status": "Success!",
               "message": "Product successfully added", "data": res}, 201
        return res


@v2.route('/<int:c_id>/products/<int:p_id>')
class ProductCategoryUpdate(Resource):

    @v2.doc(security='apikey')
    @jwt_required
    @admin_required
    def post(self, c_id, p_id):
        """
        Add a category to a product
        c_id : the category id
        p_id : the product id
        """
        store_id = get_store_id(get_jwt_identity())
        cur.execute("SELECT * FROM categories WHERE id='{}';".format(c_id))
        category = cur.fetchone()
        if not category or category[1] != store_id:
            msg = 'Category does not exist'
            return {"message":msg},404
        cur.execute("SELECT * FROM products WHERE id={};".format(p_id))
        product = cur.fetchone()
        if not product or product[1] != store_id:
            msg = 'Product does not exist'
            return {"message":msg},404
        category_name = category[2]
        cur.execute(
            "UPDATE products SET category='{}' WHERE id ='{}'".format(
                category_name, p_id))
        conn.commit()
        cur.execute("SELECT * FROM products WHERE id={};".format(p_id))
        new_p = cur.fetchone()
        format_new_p = {
            "product_name": new_p[2],
            "inventory": new_p[3],
            "price": new_p[4],
            'category': new_p[5],
            'added_at': new_p[6]
        }
        return {"status": "Updated!", "product": format_new_p}, 200
