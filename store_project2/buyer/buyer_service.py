import mysql
from buyer.buyer import Buyer
from buyer.buyer_db import BuyerDB
from util.response import Response
from util.Utitilty import *
from user.user_service import UserService


class BuyerService:
    def __init__(self, db_config):
        self._db = BuyerDB(db_config)
        self.db_config = db_config

    @staticmethod
    def validation(username, password, nationality_code, address, city):
        if len(username) < 3 and len(password) < 3:
            return Response("Username and password are too short", 400, None, None)
        if len(nationality_code) < 10:
            return Response("Nationality code is too short", 400, None, None)
        if address == '' or city == '':
            return Response('Address and city must be at least one character', 400, None, None)
        return Response("OK", 200, None, None)

    def save(self, username, password, nationality_code, address, city):
        validation_result = BuyerService.validation(username, password, nationality_code, address, city)

        if validation_result.status_code == 400:
            return validation_result

        user_service = UserService(db_config=self.db_config)
        response = user_service.save(username, password, nationality_code)
        if response.status_code != 200:
            return response
        buyer_id = generate_id()
        buyer: Buyer = Buyer(response.data, address, city, buyer_id)

        try:
            return self._db.save(buyer)
        except mysql.connector.Error as e:
            return Response(f"Error saving seller: {str(e)}", 500, None, None)

    def update(self, username, address, city):
        validation_result = BuyerService.validation(username, address, city)
        if validation_result.status_code == 400:
            return validation_result

        buyer: Buyer = Buyer(username, address, city)
        try:
            return self._db.save(buyer)
        except mysql.connector.Error as e:
            return Response(f"Error saving buyer: {str(e)}", 500, None, None)

    def delete(self, buyer_id):
        try:
            return self._db.delete(buyer_id)
        except mysql.connector.Error as e:
            return Response(f"Error delete buyer: {str(e)}", 500, None, None)

    def find_purchase_history(self, buyer_id):
        try:
            purchase_history = self._db.find_purchase_history(buyer_id)
            if not purchase_history:
                return Response("No purchase history found for this buyer.", 404, None, None)
            return Response("OK", 200, purchase_history, None)
        except mysql.connector.Error as e:
            return Response(f"Error fetching purchase history: {str(e)}", 500, None, None)

    def get_list_buyers(self, nationality_code):
        try:
            return self._db.find(nationality_code)
        except mysql.connector.Error as e:
            return Response(f"Error find buyer: {str(e)}", 500, None, None)

    def get_by_buyer_id(self, buyer_id):
        try:
            return self._db.get_by_id(buyer_id)
        except mysql.connector.Error as e:
            return Response(f"Error find buyer: {str(e)}", 500, None, None)

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
