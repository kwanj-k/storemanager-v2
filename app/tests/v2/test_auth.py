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
    enew_store = {
        "name": "KidsCity2",
        "category": "Botique",
        "email": "mwangikwanj@gmail.com",
        "password": "iamroot"
    }
    login_data = {
        "email": "mwangikwanj@gmail.com",
        "password": "iamroot"
    }
    add_data = {
        "email": "mwangiaddmin@gmail.com",
        "password": "iamroot"
    }
    empty_email = {
        "email": "",
        "password": "iamroot"
    }
    empty_pass = {
        "email": "mwangiaddmin@gmail.com",
        "password": ""
    }
    invalid_credentials = {
        "email": "mwangiadssdmin@gmail.com",
        "password": "padsdhdhdhdgg"
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

    def test_signup_twice_same_name(self):
        """
        Test store signup
        """
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(signup_url,
                            data=json.dumps(self.new_store),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'Store name already exists')
        self.assertEqual(res.status_code, 409)

    def test_signup_twice_with_same_email(self):
        """
        Test store signup
        """
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(signup_url,
                            data=json.dumps(self.enew_store),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'The user already exists')
        self.assertEqual(res.status_code, 409)

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

    def test_login_with_empty_email(self):
        """Test login_with_empty_email"""
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(login_url,
                            data=json.dumps(self.empty_email),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(res1['message'], 'The email field can not be empty')
        self.assertEqual(res.status_code, 400)

    def test_login_with_empty_password(self):
        """Test login_with_empty_password"""
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(login_url,
                            data=json.dumps(self.empty_pass),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(
            res1['message'],
            'The password field can not be empty')
        self.assertEqual(res.status_code, 400)

    def test_login_with_invalid_credentials(self):
        """Test login_with_invalid_credentials"""
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        res = self.app.post(login_url,
                            data=json.dumps(self.invalid_credentials),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(
            res1['message'],
            'Invalid credentials.If new,create a store first')
        self.assertEqual(res.status_code, 400)

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

    def test_add_existing_admin_to_admin(self):
        """
        Test add_existing_admin_to_admin
        """
        login = self.autheniticate()
        token = json.loads(login.data.decode()).get('token')
        self.app.post(admin_url,
                      data=json.dumps(self.add_data),
                      headers=dict(Authorization="Bearer " + token),
                      content_type='application/json')
        res = self.app.post(admin_url,
                            data=json.dumps(self.add_data),
                            headers=dict(Authorization="Bearer " + token),
                            content_type='application/json')
        res1 = json.loads(res.data.decode())
        self.assertEqual(
            res1['message'],
            'User already exists and is Admin already')
        self.assertEqual(res.status_code, 409)

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
