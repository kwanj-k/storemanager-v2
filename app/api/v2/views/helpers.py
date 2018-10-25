"""
This will contain common db operations
"""

#Local imports
from app.api.v2.db_config import conn

#cursor to perform database operations
cur = conn.cursor()

def get_user_by_email(email):
    """
    Looking for user using email in the database 
    """
    cur.execute("SELECT * FROM users WHERE email='{}';".format(email))
    user = cur.fetchone()
    return user

def get_store_by_name(name):
    """
    Looking up store by name in the database 
    """
    cur.execute("SELECT * FROM stores WHERE name='{}';".format(name))
    store = cur.fetchone()
    return store

def get_store_id(email):
    """
    Get the store id using user email
    """
    cur.execute("SELECT * FROM users WHERE email='{}';".format(email))
    user = cur.fetchone()
    store_id = user[1]
    return store_id
    