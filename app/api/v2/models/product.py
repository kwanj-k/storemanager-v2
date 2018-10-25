"""
A model class for all product related classes
"""

# local imports
from app.api.common.utils import dt
from app.api.v2.db_config import conn


# cursor to perform database operations
cur = conn.cursor()


class Product:
    """
    The product definition
    """
    cat = 'Category-not-set'

    def __init__(self, store_id, name, inventory, price,):
        """
        Product constructor
        """
        self.store_id = store_id
        self.name = name
        self.inventory = inventory
        self.price = price
        self.category = Product.cat
        self.created_at = dt

    def add_product(self):
        """
        Add product method
        """
        product = """INSERT INTO
                products  (store_id,name, inventory,price,category,created_at)
                VALUES ('%s','%s','%s','%s','%s','%s')"""\
                 % (self.store_id, self.name, self.inventory, self.price, self.category, self.created_at)
        cur.execute(product)
        conn.commit()

    def json_dump(self):
        """
        custom json_dump method to return a custom python dict in response
       """
        return dict(
            name=self.name,
            inventory=self.inventory,
            price=self.price,
            category=self.category,
            created_at=self.created_at
        )
