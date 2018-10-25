"""
A module to contain all sale related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

cart_url = "api/v2/cart"
product_url = "/api/v2/products"
add_to_cart_url ="/api/v2/products/1"
sales_url = "api/v2/sales"

class TestSales(Settings):
    data = {
        "number": 3
    }
    product_data = {
        "name": "monster34w",
        "inventory": 24,
        "price": 165
    }
    def test_get_sales(self):
        """Test for  get sales endpoint."""
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
        self.app.post(cart_url,
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res = self.app.get(sales_url,
                           headers=dict(Authorization="Bearer " + token),
                           content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'],'Success!')
        self.assertEqual(res.status_code, 200)
