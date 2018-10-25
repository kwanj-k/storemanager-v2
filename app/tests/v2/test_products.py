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

    def test_product_addition(self):
        """Test for the add product endpoint."""
        res = self.app.post(product_url,
                            data=json.dumps(self.data),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'],'Producted added')
        self.assertEqual(res.status_code, 201)

    def test_get_all_products(self):
        """Test for the get all products endpoint."""

        self.app.post(product_url,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get(product_url)
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'],'Success!')
        self.assertEqual(res.status_code, 200)

    def test_get_product_by_id(self):
        """Test for the get product by id endpoint."""

        self.app.post(product_url,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get("/api/v2/products/1")
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'],'Success!')
        self.assertEqual(res.status_code, 200)

    def test_product_update(self):
        """Test for the product update endpoint."""

        self.app.post(product_url,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.put('/api/v2/products/1',
                           data=json.dumps(self.pdata),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'],'Updated!')
        self.assertEqual(res.status_code, 200)

    def test_product_delete(self):
        """Test for the product delete endpoint."""
        self.app.post(product_url,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.delete('/api/v2/products/1',
                              content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'],'Deleted!')
        self.assertEqual(res.status_code, 200)
