import uuid
from util.response import Response
from product.product_db import ProductDB as db
from product.Product import Product
from seller.seller import Seller


def generate_id() -> str:
    return str(uuid.uuid4())


class ProductService:
    def __init__(self):
        self.products = []

    @staticmethod
    def validation(name: str, price: float, model: str) -> Response:
        if len(model and name) > 3:
            if price <= 0:
                return Response("NOT_OK", 602, None, "Price must be greater than 0.")
            return Response("OK", 200, None, "Validation successful.")
        return Response("NOT_OK", 601, None, "Model or Name is not valid.")

    def create_product(self, name: str, price: float, model: str, seller: Seller) -> Response:
        # Check the seller
        if not seller or not isinstance(seller, Seller):
            return Response("NOT_OK", 601, None, "User must be logged in as a seller.")

        valid_response = self.validation(name, price, model)
        if valid_response.status != "OK":
            return valid_response

        product_id = generate_id()
        product = Product(product_id, name, price, model, seller)
        self.products.append(product)
        db.save(product)
        return Response("OK", 200, product, "Product created successfully.")

    def read_all_products(self):
        if not self.products:
            print("No products available.")
            return

        for product in self.products:
            print(product)

    def update_product(self, product_id: str, name: str = None, price: float = None, model: str = None) -> Response:
        product = self.find_product(product_id)
        if product:
            if name is not None:
                product.name = name
            if price is not None and price > 0:
                product.price = price
            if model is not None and len(model) > 3:
                product.model = model

            db.save(product)  # Update the database after modification
            return Response("OK", 200, product, f"Product {product_id} updated successfully.")
        return Response("NOT_OK", 603, None, f"Product with ID {product_id} not found.")

    def delete_product(self, product_id: str) -> Response:
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            db.delete(product_id)  # Assuming 'delete' method requires product_id
            return Response("OK", 200, None, f"Product {product_id} deleted successfully.")
        return Response("NOT_OK", 603, None, f"Product with ID {product_id} not found.")

    def find_product(self, product_id: str) -> Product or None:
        return next((product for product in self.products if product.product_id == product_id), None)

    def __getitem__(self, index):
        return self.products[index]

    def __iter__(self):
        return iter(self.products)
