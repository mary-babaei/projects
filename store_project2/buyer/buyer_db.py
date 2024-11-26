import mysql.connector
from util.response import *
from buyer.buyer import Buyer
from initial import *


class BuyerDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def initial(self):
        create_table_users(self.connection)
        create_table_seller(self.connection)
        create_table_buyer(self.connection)
        create_table_products(self.connection)
        create_table_factor(self.connection)

    def save(self, buyer: Buyer) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''INSERT INTO products.TBL_BUYERS (address, city, buyer_id, user_id) 
            values (%s, %s, %s, %s)'''
            value = (buyer.address, buyer.city, buyer.buyer_id, buyer.user.id)
            cursor.execute(query, value)
            self.connection.commit()

            return Response("Saved successfully", 200, {buyer}, "save successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, {buyer}, "save unsuccessful")

    def find(self, nationality_code) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''SELECT * FROM products.TBL_BUYERS where nationality_code = %s'''
            value = (nationality_code,)
            cursor.execute(query, value)
            # return cursor.fetchone()
            return Response("find successfully", 200, f"{cursor.fetchone()}",
                            "successfully")
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def get_by_id(self, buyer_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''SELECT * FROM products.TBL_BUYERS where buyer_id = %s'''
            value = (buyer_id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("Success", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def update(self, username, address, city, buyer_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''UPDATE products.TBL_BUYERS SET address = %s, city = %s, username = %s WHERE buyer_id = %s'''
            value = (address, city, username, buyer_id)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("Update successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def delete(self, buyer_id) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''DELETE FROM products.TBL_BUYERS WHERE buyer_id = %s'''
            value = (buyer_id,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("Delete successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Connection Error {err}")
            return Response("Connection Error", 500, None, None)
        finally:
            cursor.close()

    def get_by_username_and_password(self, username, password) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_SELLERS WHERE username = %s and password = %s'''
            value = (username, password)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("get_by_username_and_password successfully", 200,
                            f"{cursor.fetchone()}", "successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("get_by_username_and_password Error", 500, None, None)
        finally:
            cursor.close()

    def get_by_nationality_code(self, nationality_code) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_SELLERS WHERE nationality_code = %s '''
            value = (nationality_code,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("get-by_nationality-code successfully", 200, None, None)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("get_by_nationality-code Error", 500, None, None)
        finally:
            cursor.close()

    def find_purchase_history(self, buyer_id):
        cursor = self.connection.cursor()
        try:
            query = '''SELECT 
                f.factor_id,
                f.date,
                p.name
            FROM 
                TBL_PRODUCT_FACTORS f
            JOIN 
                TBL_BUYERS b ON f.buyer_id = b.buyer_id
            JOIN 
                TBL_PRODUCTS p ON f.product_id = p.id
            WHERE 
                b.buyer_id = %s
            '''
            value = (buyer_id,)
            cursor.execute(query, value)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("find_purchase_history Error", 500, None, None)
        finally:
            cursor.close()