from util.response import Response
import mysql

class FinancialDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def create(self, seller, buyer, product, factor_id) -> Response:
        try:
            cursor = self.connection.cursor()
            query = ''' INSERT INTO financial (seller, buyer, product, factor_id) VALUES (%s, %s, %s, %s)'''
            values = (seller, buyer, product, factor_id)
            cursor.execute(query, values)
            self.connection.commit()
            return Response("OK", 200, seller, 'Saved successfully')
        except mysql.connection.Error as err:
            print(f"Connection Error {err}")
            return Response("Not OK", 500, seller, 'Connection Error')

    def delete(self, factor_id) -> Response:
        try:
            cursor = self.connection.cursor()
            query = '''DELETE FROM financial WHERE factor_id=%s'''
            values = (factor_id,)
            cursor.execute(query, values)
            self.connection.commit()
            return Response("OK", 200, factor_id, 'Deleted successfully')
        except mysql.connection.Error as err:
            print(f"Connection Error {err}")
            return Response("Not OK", 500, factor_id, 'Connection Error')

    def get_factor_details(self, factor_id) -> Response:
        try:
            cursor = self.connection.cursor()
            query = '''SELECT * FROM financial WHERE factor_id=%s'''
            values = (factor_id,)
            cursor.execute(query, values)
            self.connection.commit()
            return Response("OK", 200, factor_id)
        except mysql.connection.Error as err:
            print(f"Connection Error {err}")
            return Response("Not OK", 500, factor_id, 'Connection Error')

    def find(self, factor_id) -> Response:
        try:
            cursor = self.connection.cursor()
            query = '''SELECT * FROM financial WHERE factor_id=%s'''
            values = (factor_id,)
            cursor.execute(query, values)
            self.connection.commit()
            return Response("OK", 200, factor_id)
        except mysql.connectin.Error as err:
            print(f"Connection Error {err}")
            return Response("Not OK", 500, factor_id)
