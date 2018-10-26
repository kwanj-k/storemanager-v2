"""
A model class for Sale
"""

# local imports
from app.api.common.utils import dt
from app.api.v2.db_config import conn
from app.api.v2.models.cart import Cart


# cursor to perform database operations
cur = conn.cursor()


class Sale(Cart):
    """
    Sale object which inherites some of its attributes from cart
    """

    def __init__(self, store_id, seller_id, product, number, amount):
        super().__init__(
            seller_id=seller_id,
            product=product,
            number=number,
            amount=amount)
        self.store_id = store_id
        self.created_at = dt

    def sell(self):
        """
        The sell sql query
        """
        sale = """INSERT INTO
                sales  (store_id,seller_id,product, number,amount,created_at)
                VALUES
                ('%s','%s','%s','%s','%s','%s')""" \
                % (self.store_id, self.seller_id, self.product, self.number, self.amount, self.created_at)
        cur.execute(sale)
        conn.commit()
