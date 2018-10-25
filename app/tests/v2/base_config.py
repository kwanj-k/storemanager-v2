"""
This will contain the base tests configuration.
Thi will be reused/imported in almost all the tests.

"""
# Standard library imports
import unittest
import json

# Local application imports
from app.apps import create_app
from app.api.v2.db_config import create_tables,drop_all


config_name = "testing"
app = create_app(config_name)

login_url = "/api/v2/auth/login"
signup_url = "/api/v2/signup"

class Settings(unittest.TestCase):
    """
    Settings class to hold all the similar test config
    """

    new_store = {
        "name": "Ctrim",
        "category": "wholesale",
        "email": "ces@ces.com",
        "password": "iamroot"
    }
    login_data = {
        "email": "ces@ces.com",
        "password": "iamroot"
    }

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        create_tables()

    def autheniticate(self):
        self.app.post(signup_url,
                      data=json.dumps(self.new_store),
                      content_type='application/json')
        return self.app.post(login_url,
                             data=json.dumps(self.login_data),
                             content_type='application/json')

    def tearDown(self):
        drop_all()
