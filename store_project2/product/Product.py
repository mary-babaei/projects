from seller.seller import Seller


class Product:
    def __init__(self, product_id: int, name: str, price: float, model: str, seller: Seller):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.model = model
        self.seller = seller

    def __str__(self):
        return (
            f"ID: {self.product_id}, Name: {self.name}, Price: {self.price}, model: {self.model},"
            f" seller: {self.seller.nationality_code}")
