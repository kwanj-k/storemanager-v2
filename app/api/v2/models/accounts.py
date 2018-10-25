"""
A model class for all account related classes
i.e the store and user
"""

#Third party imports
from werkzeug.security import generate_password_hash

#local imports
from app.api.common.utils import dt
from app.api.v2.db_config import conn


#cursor to perform database operations
cur = conn.cursor()

class Store:
    """
    The store definition
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.created_at = dt

    def create_store(self):
        store = """INSERT INTO
                stores  (name, category,created_at)
                VALUES ('%s','%s','%s')""" % (self.name,self.category,self.created_at)
        cur.execute(store)
        conn.commit()

    def json_dump(self):
        """
        custom json_dump method to return a custom python dict in response
       """
        return dict(
            name=self.name,
            category=self.category,
            created_at = self.created_at
        )

class User:
    """
    The definition of a user
    """
    
    def __init__(self, store_id,role, email, password):
        self.store_id = store_id
        self.role = role
        self.email = email
        self.password = generate_password_hash(password)
        self.added_at = dt

    def create_user(self):
        user = """INSERT INTO
                users  (store_id, role, email, password,added_at)
                VALUES ('{}','{}','{}','{}','{}')""" \
                .format(self.store_id,self.role,self.email,self.password,self.added_at)
        cur.execute(user)
        conn.commit()

    def json_dump(self):
        """
        custom json_dump method to return a custom python dict in response
        """
        def rank():
            if self.role==0:
                rank = 'SuperAdmin'
            if self.role==1:
                rank = 'Admin'
            if self.role==2:
                rank = 'Attendant'
            return rank
        return dict(
            email=self.email,
            role=rank(),
            added_at = self.added_at)
            