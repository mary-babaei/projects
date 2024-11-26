from datetime import datetime
from product import Product
from seller.seller import Seller
from buyer.buyer import Buyer


class ProductFinancial:
    def __init__(self, seller: Seller, buyer: Buyer, product: Product, factor_id):
        self.seller = seller
        self.buyer = buyer
        self.product = product
        self.factor_id = factor_id
        self.created_date = datetime.now(datetime)

    def __str__(self):
        return f'{self.factor_id}: {self.seller} - {self.buyer} - {self.product}'
