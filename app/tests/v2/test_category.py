"""
A module to contain all category related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

category_url = "api/v2/categories"
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
        self.assertEqual(res1['status'],'Success!')
        self.assertEqual(res.status_code, 201)

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
        self.assertEqual(res1['status'],'Success!')
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res1['status'],'Updated!')
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res1['status'],'Deleted!')
        self.assertEqual(res.status_code, 200)

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
        self.assertEqual(res1['status'],'Updated!')
        self.assertEqual(res.status_code, 200)
