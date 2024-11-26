from seller.seller import Seller
from util.response import Response
from seller.seller_db import SellerDB
from util.Utitilty import generate_id
import mysql.connector
from user.user_service import UserService


class SellerService:
    def __init__(self, cfg):
        self._db = SellerDB(cfg)
        self.config = cfg

    @staticmethod
    def validation(username, password, nationality_code, shop_name) -> Response:
        if len(username) < 3 and len(password) < 3:
            return Response("Username and password are too short", 400, None, None)
        if len(nationality_code) < 10:
            return Response("Nationality code is too short", 400, None, None)
        if len(shop_name) < 3:
            return Response("Shop name must be at least 3 characters.", 400, None, None)
        return Response("OK", 200, None, None)

    def save(self, username, password, nationality_code, shop_name):
        validation_result = SellerService.validation(username, password, nationality_code, shop_name)
        if validation_result.status_code == 400:
            return validation_result

        user_service = UserService(db_config=self.config)
        response = user_service.save(username, password, nationality_code)
        if response.status_code != 200:
            return response
        shoping_id = generate_id()
        seller: Seller = Seller(shop_name, shoping_id, response.data)
        try:
            return self._db.save(seller)
        except mysql.connector.Error as e:
            return Response(f"Error saving seller: {str(e)}", 500, None, None)

    def update(self, username):
        validation_result = SellerService.validation(username)
        if validation_result.status_code == 400:
            return validation_result

        seller = Seller(username)
        try:
            return self._db.update(seller)
        except mysql.connector.Error as e:
            return Response(f"Error updating seller: {str(e)}", 500, None, None)

    def delete(self, nationality_code):
        try:
            return self._db.delete(nationality_code)
        except mysql.connector.Error as e:
            return Response(f"Error delete seller: {str(e)}", 500, None, None)

    def search_by_shoping_id(self, shoping_id):
        try:
            return self._db.get_by_shoping_id(shoping_id)
        except mysql.connector.Error as e:
            return Response(f"Error search seller: {str(e)}", 500, None, None)

    def search_by_nationality_code(self, nationality_code):
        try:
            return self._db.find(nationality_code)
        except mysql.connector.Error as e:
            return Response(f"Error search seller: {str(e)}", 500, None, None)

    def search_by_username(self, username):
        try:
            return self._db.get_by_username_and_password(username)
        except mysql.connector.Error as e:
            return Response(f"Error search seller: {str(e)}", 500, None, None)

    def search_by_password(self, password):
        try:
            return self._db.get_by_username_and_password(password)
        except mysql.connector.Error as e:
            return Response(f"Error search seller: {str(e)}", 500, None, None)
