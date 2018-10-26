"""
A module to contain all authorisation related test cases
"""
# Standard library imports
import json

# Local application imports
from .base_config import Settings

login_url = "/api/v2/auth/login"
signup_url = "/api/v2/signup"
admin_url = "/api/v2/admin"
attendant_url = "/api/v2/attendant"


class TestAuth(Settings):
    new_store = {
        "name": "KidsCity",
        "category": "Botique",
        "email": "mwangikwanj@gmail.com",
        "password": "iamroot"
    }
    login_data = {
        "email": "mwangikwanj@gmail.com",
        "password": "iamroot"
    }
    add_data = {
        "email": "mwangiadd@gmail.com",
        "password": "iamroot"
    }

    def test_signup(self):
        """
        Test store signup
        """
        res = self.app.post(signup_url,
                            data=json.dumps(self.new_store),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Store successfully created')
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        """Test for the login endpoint."""
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(login_url,
                            data=json.dumps(self.login_data),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 200)

    def test_addadmin(self):
        """
        Test add admin
        """
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')

        res = self.app.post(admin_url,
                            data=json.dumps(self.add_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 201)

    def test_addattendant(self):
        """
        Test add attendant
        """
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        res = self.app.post(attendant_url,
                            data=json.dumps(self.login_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['status'], 'Success!')
        self.assertEqual(res.status_code, 201)
