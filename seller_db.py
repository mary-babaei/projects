import mysql.connector
from seller.seller import Seller
from util.response import *

class SellerDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def save(self, seller: Seller) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''INSERT INTO products.TBL_SELLERS(shop_name, shoping_id, user_id) 
            values (%s, %s, %s)'''
            value = (seller.shop_name, seller.shoping_id, seller.user.id)
            cursor.execute(query, value)
            self.connection.commit()
            generated_id = cursor.lastrowid
            seller.id = generated_id
            return Response("OK", 200, seller, 'Saved successfully')
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, seller, str(err))
        finally:
            cursor.close()

    def delete(self, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' DELETE FROM products.TBL_SELLERS where shoping_id = %s '''
            value = (shoping_id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("deleted successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def get_all(self, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''SELECT * FROM products.TBL_SELLERS where shoping_id = %s'''
            value = (shoping_id,)
            cursor.execute(query, value)
            # return cursor.fetchall()
            return Response("get_all successfully", 200, f"{cursor.fetchall()}",
                            "successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def update(self, shop_name, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''update products.TBL_SELLERS set shop_name = %s WHERE shoping_id = %s'''
            value = (shop_name, shoping_id)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("updated successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response(f"Connection Error", 500, None, None)
        finally:
            cursor.close()

    def find(self, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''SELECT * FROM products.TBL_SELLERS where shoping_id = %s'''
            value = (shoping_id,)
            cursor.execute(query, value)
            # return cursor.fetchone()
            return Response("find successfully", 200, f"{cursor.fetchone()}",
                            "successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def get_by_shoping_id(self, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_SELLERS WHERE shoping_id = %s'''
            value = (shoping_id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("get_by_shoping_id successfully", 200,
                            f"{cursor.fetchone()}", "successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("get_by_shoping_id Error", 500, None, None)
        finally:
            cursor.close()

    def get_by_nationality_code(self, shoping_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_SELLERS WHERE shoping_id = %s '''
            value = (shoping_id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("get-by_nationality-code successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("get_by_nationality-code Error", 500, None, None)
        finally:
            cursor.close()