"""
 App module to bring together the whole app.

"""

# Standard library import
import os
from datetime import timedelta

# Third party imports
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

# Local imports
from .api.v2.db_config import create_tables, drop_all
from instance.config import app_config
from .api.v2.db_config import conn


jwt = JWTManager()
mail = Mail()
secret_key = os.getenv('SECRET')
password = os.getenv('PASSWORD')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    #drop_all()
    create_tables()
    app.config['JWT_SECRET_KEY'] = secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=72)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'storemanager.api@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'storemanager.api@gmail.com'
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    cur = conn.cursor()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        cur.execute("SELECT * FROM tokens WHERE token='{}';".format(jti))
        black_token = cur.fetchone()
        return black_token

    from .api.v2.routes import v_2 as v2
    from .api.v2.routes import v2 as jwtapi
    app.register_blueprint(v2)
    jwt._set_error_handler_callbacks(jwtapi)

    return app
