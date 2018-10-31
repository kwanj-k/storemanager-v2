"""
A module to contain all category related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

category_url = "api/v2/categories"
addnew_product_to_category_url = "api/v2/categories/1/products"
product_url = "/api/v2/products"
productcategory_url = "/api/v2/categories/1/products/1"


class TestCategories(Settings):
    data = {
        "name": "Drinks"
    }
    pdata = {
        "name": "SoftDrinks"
    }
    product_data = {
        "name": "monster34w",
        "inventory": 24,
        "price": 165
    }

    def test_category_addition(self):
        """Test for the add category endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(category_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 201)

    def test_category_addition_twice(self):
        """Test for the add category endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(category_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Category already exists')
        self.assertEqual(res.status_code, 409)

    def test_get_all_categories(self):
        """Test for the get all categories endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.get(category_url,
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 200)

    def test_get_categories_without_any_added(self):
        """Test for get_categories_without_any_added."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.get(category_url,
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(
            res1['message'],
            'There are no categories at this time')
        self.assertEqual(res.status_code, 404)

    def test_category_update(self):
        """Test for the category update endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.put('/api/v2/categories/1',
                           data=json.dumps(self.pdata),
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Updated!')
        self.assertEqual(res.status_code, 200)

    def test_category_update_to_existing_category(self):
        """Test category_update_to_existing_category."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        self.app.post(category_url,
                      data=json.dumps(self.pdata),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.put('/api/v2/categories/1',
                           data=json.dumps(self.pdata),
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'That category already exists')
        self.assertEqual(res.status_code, 406)

    def test_non_existing_category_update(self):
        """Test non_existing_category_update."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.put('/api/v2/categories/1',
                           data=json.dumps(self.pdata),
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Category does not exist')
        self.assertEqual(res.status_code, 404)

    def test_category_delete(self):
        """Test for the category delete endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.delete('/api/v2/categories/1',
                              headers=dict(Authorization="Bearer " + token),
                              content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Deleted!')
        self.assertEqual(res.status_code, 200)

    def test_delete_non_existing_category(self):
        """Test delete_non_existing_category."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.delete('/api/v2/categories/1',
                              headers=dict(Authorization="Bearer " + token),
                              content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Category does not exist')
        self.assertEqual(res.status_code, 404)

    def test_add_category_to_product(self):
        """Test the add category to a product"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.product_data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(productcategory_url,
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Updated!')
        self.assertEqual(res.status_code, 200)

    def test_add_non_existing_category_to_product(self):
        """Test add_non_existing_category_to_product"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.product_data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(productcategory_url,
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Category does not exist')
        self.assertEqual(res.status_code, 404)

    def test_add_category_to_non_existing_product(self):
        """Test add_category_to_non_existing_product"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(productcategory_url,
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product does not exist')
        self.assertEqual(res.status_code, 404)

    def test_add_new_product_to_category(self):
        """Test the add add_new_product_to_category"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(addnew_product_to_category_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product successfully added')
        self.assertEqual(res.status_code, 201)

    def test_add_new_product_to_non_existing_category(self):
        """Test add_new_product_to_non_existing_category"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(addnew_product_to_category_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Category does not exist')
        self.assertEqual(res.status_code, 404)

    def test_add_existing_product_category(self):
        """Test add_existing_product_category"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.product_data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        self.app.post(category_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(addnew_product_to_category_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(
            res1['message'],
            'Product already exists.Update product inventory instead')
        self.assertEqual(res.status_code, 409)
