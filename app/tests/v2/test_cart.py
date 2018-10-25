"""
A module to contain all cart related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

cart_url = "api/v2/cart"
product_url = "/api/v2/products"
add_to_cart_url ="/api/v2/products/1"
cart_update_url = "api/v2/cart/1"

class TestCart(Settings):
    data = {
        "number": 3
    }
    pdata = {
        "number": 2
    }
    product_data = {
        "name": "monster34w",
        "inventory": 24,
        "price": 165
    }

    def test_add_to_cart(self):
        """Test for the add to cart endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Added to cart')
        self.assertEqual(res.status_code, 200)

    def test_get_cart(self):
        """Test for the get cart endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.get(cart_url,
                        headers=dict(Authorization="Bearer " + token))
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Success!')
        self.assertEqual(res.status_code, 200)

    def test_cart_update(self):
        """Test for the cart update endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.put(cart_update_url,
                           data=json.dumps(self.pdata),
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Cart Updated')
        self.assertEqual(res.status_code, 200)

    def test_delete_product_from_cart(self):
        """Test for the delete product from cart endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.delete(cart_update_url,
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Deleted!')
        self.assertEqual(res.status_code, 200)

    def test_delete_an_entire_cart(self):
        """Test for the delete entire cart endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.delete(cart_url,
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Cart Deleted!')
        self.assertEqual(res.status_code, 200)

    def test_sell_cart(self):
        """Test for  sell cart endpoint."""
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(product_url,
                            data=json.dumps(self.product_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        self.app.post(add_to_cart_url,
                            data=json.dumps(self.data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res = self.app.post(cart_url,
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Sold!')
        self.assertEqual(res.status_code, 201)
