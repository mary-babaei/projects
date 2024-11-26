import mysql.connector
from user.User import User
from util.response import Response


class UserDB:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
            host=db_config.get('DATABASE', 'host'),
            port=db_config.get('DATABASE', 'port'),
            user=db_config.get('DATABASE', 'user'),
            password=db_config.get('DATABASE', 'password'),
        )

    def save(self, user: User) -> Response:
        cursor = self.connection.cursor()
        try:
            query = '''INSERT INTO products.TBL_USERS(username, password, nationality_code) VALUES (%s, %s, %s)'''
            value = (user.username, user.password, user.nationality_code)
            cursor.execute(query, value)
            self.connection.commit()
            generated_id = cursor.lastrowid
            user.id = generated_id
            return Response("ok", 200, user, "save successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, user, "save failed")
        finally:
            cursor.close()

    def update(self, username, password) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' UPDATE products.TBL_USERS SET username = (%s), password =(%s) WHERE nationality_code = (%s)'''
            value = (username, password)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, {username, password}, "update successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, {username, password}, "update failed")
        finally:
            cursor.close()

    def get_by_nationality_code(self, nationality_code) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_USERS WHERE nationality_code = %s'''
            value = (nationality_code,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, {nationality_code}, "get successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, {nationality_code}, "get failed")
        finally:
            cursor.close()

    def get_by_username_password(self, username, password) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' SELECT * FROM products.TBL_USERS WHERE username = %s and password = %s'''
            value = (username, password)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, {username, password}, "get successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, {username, password}, "get failed")
        finally:
            cursor.close()

    def delete(self, nationality_code) -> Response:
        cursor = self.connection.cursor()
        try:
            query = ''' DELETE FROM products.TBL_USERS WHERE nationality_code = %s'''
            value = (nationality_code,)
            cursor.execute(query, value)
            self.connection.commit()
            return Response("ok", 200, {nationality_code}, "delete successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return Response("Not OK", 500, {nationality_code}, "delete failed")
        finally:
            cursor.close()
