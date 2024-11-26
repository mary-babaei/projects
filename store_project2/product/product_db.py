import mysql.connector
from product.Product import Product


class ProductDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def save(self, product: Product) -> bool:
        try:
            cursor = self.connection.cursor()
            query = '''insert into mst.TBL_PRODUCTS(product_id, name, price, model, seller_id)
             values (%s, %s, %s, %s, %s)'''
            value = (product.product_id, product.name, product.price, product.model, product.seller.id)
            cursor.exeute(query, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return False
        finally:
            cursor.close()

    def delete(self, product_id):
        cursor = self.connection.cursor()
        try:
            query = '''delete from tbl_product where id = %s'''
            value = (id,)
            cursor.exeute(query, value)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()  # بستن اتصال

    def update(self, price) -> Product:
        cursor = self.connection.cursor()
        try:
            query = '''UPDATE tbl_product set price = %s'''
            value = (price,)
            cursor.exeute(query, value)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
