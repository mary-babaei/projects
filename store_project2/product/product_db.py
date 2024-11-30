from itertools import product

import mysql.connector
from product.Product import Product
from util.response import Response

class ProductDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def save(self, product: Product) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''INSERT INTO products.TBL_PRODUCTS(id, name, price, model, seller_id)
                   VALUES (%s, %s, %s, %s, %s)'''
            values = (product.product_id, product.name, product.price, product.model, product.seller.id)
            cursor.execute(query, values)
            self.connection.commit()
            return Response("ok", 200, product, "save product successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, product, "save product failed")
        finally:
            cursor.close()

    def delete(self, id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''delete from products.TBL_PRODUCTS where id = %s'''
            value = (id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, product, "delete product successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, product, "delete product failed")
        finally:
            cursor.close()

    def update(self, price: float) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''UPDATE products.TBL_PRODUCTS set price = %s where id = %s'''
            value = (price,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, product, "update product successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, product, "update product failed")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

    def __del__(self):
        """Ensure the connection is closed when the object is deleted."""
        self.close_connection()
