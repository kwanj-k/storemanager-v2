"""
A module to contain all product related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

product_url = "/api/v2/products"


class TestProducts(Settings):
    data = {
        "name": "monster",
        "inventory": 24,
        "price": 165
    }
    pdata = {
        "name": "monsterupdate",
        "inventory": 12,
        "price": 180
    }
    unwanted_data = {
        "test": "test",
        "name": "monsterupdate",
        "inventory": 12,
        "price": 180
    }
    less_data = {
        "inventory": 12,
        "price": 180
    }
    empty_data = {
        "name": "",
        "inventory": 12,
        "price": 180
    }

    def test_product_addition(self):
        """Test for the add product endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(product_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product successfully added')
        self.assertEqual(res.status_code, 201)

    def test_product_addition_with_unwanted_data(self):
        """Test product_addition_with_unwanted_data"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(product_url,
                            data=json.dumps(self.unwanted_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'The field test is not required')
        self.assertEqual(res.status_code, 400)

    def test_product_addition_with_less_data(self):
        """Test product_addition_with_less_data"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(product_url,
                            data=json.dumps(self.less_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Please provide the name field')
        self.assertEqual(res.status_code, 400)

    def test_product_addition_with_empty_data(self):
        """Test product_addition_with_empty_data"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(product_url,
                            data=json.dumps(self.empty_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'The name can not be empty')
        self.assertEqual(res.status_code, 400)

    def test_product_addition_twice(self):
        """Test product_addition_twice"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.post(product_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product already exists.Update product inventory instead')
        self.assertEqual(res.status_code, 409)

    def test_get_all_products(self):
        """Test for the get all products endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.get(product_url,
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 200)

    def test_get_all_products_when_no_products(self):
        """Test get_all_products_when_no_products"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.get(product_url,
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'There are no products at the moment')
        self.assertEqual(res.status_code, 404)

    def test_get_product_by_id(self):
        """Test for the get product by id endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.get("/api/v2/products/1",
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 200)

    def test_get_non_existing_product_by_id(self):
        """Test get_non_existing_product_by_id"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.get("/api/v2/products/1",
                           headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product does not exist')
        self.assertEqual(res.status_code, 404)

    def test_product_update(self):
        """Test for the product update endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.put('/api/v2/products/1',
                           headers=dict(Authorization="Bearer " + token),
                           data=json.dumps(self.pdata),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Updated!')
        self.assertEqual(res.status_code, 200)

    def test_product_update_to_existing_product(self):
        """Test product_update_to_existing_product"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        self.app.post(product_url,
                      data=json.dumps(self.pdata),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.put('/api/v2/products/1',
                           headers=dict(Authorization="Bearer " + token),
                           data=json.dumps(self.pdata),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'That product already exists')
        self.assertEqual(res.status_code, 406)


    def test_non_existing_product_update(self):
        """Test non_existing_product_update"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.put('/api/v2/products/1',
                           headers=dict(Authorization="Bearer " + token),
                           data=json.dumps(self.pdata),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product does not exist')
        self.assertEqual(res.status_code, 404)

    def test_product_delete(self):
        """Test for the product delete endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.delete('/api/v2/products/1',
                              headers=dict(Authorization="Bearer " + token),
                              content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Deleted!')
        self.assertEqual(res.status_code, 200)

    def test_non_existing_product_delete(self):
        """Test non_existing_product_delete"""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.delete('/api/v2/products/1',
                              headers=dict(Authorization="Bearer " + token),
                              content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Product does not exist')
        self.assertEqual(res.status_code, 404)
