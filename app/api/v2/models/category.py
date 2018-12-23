"""
Category definition file
"""

# local imports
from app.api.common.utils import dt
from app.api.v2.db_config import conn


# cursor to perform database operations
cur = conn.cursor()


class Category:
    """
    category class
    """

    def __init__(self, store_id, name):
        self.store_id = store_id
        self.name = name
        self.created_at = dt

    def add_category(self):
        cat = """INSERT INTO
                categories  (store_id,name,created_at)
                VALUES ('%s','%s','%s')""" % (self.store_id, self.name, self.created_at)
        cur.execute(cat)
        conn.commit()

    def json_dump(self):
        """
        custom json_dump method to return a custom python dict in response
       """
        return dict(
            name=self.name,
            created_at=self.created_at
        )
