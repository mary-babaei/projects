from util.response import Response
from product.product_db import ProductDB as db
import uuid
from product.Product import Product
from seller.seller import Seller

def generate_id() -> str:
    return str(uuid.uuid4())


class ProductService:
    def __init__(self):
        self.products = []

    @staticmethod
    def validation(name: str, price: float, model: str) -> Response:
        if len(model) <= 3:
            return Response("NOT_OK", 601, None, "Model is not Valid")
        if price <= 0:
            return Response("NOT_OK", 602, None, "Price must be greater than 0")
        return Response("OK", 200, None, "Validation Successful")

    def create_product(self, name: str, price: float, model: str, seller: Seller) -> Response:
        valid_response = self.validation(name, price, model)
        if valid_response.status != "OK":
            return valid_response
        product_id = generate_id()
        product = Product(product_id, name, price, model, seller)
        self.products.append(product)  # اضافه کردن به لیست محصولات
        db.save(product)
        return Response("OK", 200, product, "Product created successfully.")

    def read_all_products(self):
        if not self.products:
            print("No products available.")
            return
        for product in self.products:
            print(product)

    def update_product(self, product_id: int, name: str = None, price: float = None, model: str = None):
        product = self.find_product(product_id)
        if product:
            if name is not None:
                product.name = name
            if price is not None and price > 0:  # اعتبارسنجی قیمت
                product.price = price
            if model is not None and len(model) > 3:  # اعتبارسنجی مدل
                product.model = model
            print(f"Product {id} updated successfully.")
            db.save(product)
        else:
            print(f"Product with ID {id} not found.")

    def delete_product(self, product_id: int):
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            print(f"Product {product_id} deleted successfully.")
            db.delete(product)
        else:
            print(f"Product with ID {id} not found.")

    def find_product(self, product_id: int) -> Product or None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

