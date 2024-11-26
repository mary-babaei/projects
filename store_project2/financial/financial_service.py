import mysql
from seller.seller import Seller
from buyer.buyer import Buyer
from product.Product import Product
from util.Utitilty import generate_id
from util.response import Response


class FinancialService:
    def __init__(self, seller: Seller, buyer: Buyer, product: Product):
        self.seller = seller
        self.buyer = buyer
        self.product = product

    factor_id = generate_id()

    def create(self, seller, buyer, product, factor_id) -> Response:
        if self.find(factor_id):
            print("Factor already exists")
            return Response("not ok", 400, {factor_id}, "Factor already exists")
        else:
            factor = self.create(seller, buyer, product, factor_id)
        return Response('ok!', 200, {factor_id: factor}, 'Factor created!')

    def delete(self, factor_id) -> Response:
        if self.find(factor_id):
            self.delete(factor_id)
            print("Factor deleted")
            return Response("ok", 200, {factor_id}, "Factor deleted")
        else:
            return Response("not ok", 400, {None}, "Factor not found")

    def get_factor_details(self, factor_id) -> Response:
        if self.find(factor_id):
            self.get_factor_details(factor_id)
            print("Factor details")
            return Response("ok", 200, {factor_id}, "Factor details")
        else:
            return Response("not ok", 400, {None}, "Factor not found")

    def find(self) -> str | Response:
        try:
            return self.factor_id
        except mysql.connector.Error as err:
            return Response("not ok", 400, {None}, "Factor already exists")
