"""
cart definition class
"""

# local imports
from app.api.common.utils import dt
from app.api.v2.db_config import conn


# cursor to perform database operations
cur = conn.cursor()


class Cart:
    def __init__(self, seller_id, product, number, amount):
        """
        Cart constructor
        """
        self.seller_id = seller_id
        self.product = product
        self.number = number
        self.amount = amount
        self.created_at = dt

    def add_to_cart(self):
        item = """INSERT INTO
                carts  (seller_id,product, number,amount,created_at)
                VALUES
                ('%s','%s','%s','%s','%s')"""\
                 % (self.seller_id, self.product, self.number, self.amount, self.created_at)
        cur.execute(item)
        conn.commit()

    def json_dump(self):
        """
        custom json_dump method to return a custom python dict in response
        """
        return dict(
            product=self.product,
            number=self.number,
            amount=self.amount,
            created_at=self.created_at
        )
