from user.user_db import UserDB
from util.response import Response
from user.User import User
from util.Utility import hash_password


class UserService:
    def __init__(self, db_config):
        self._db = UserDB(db_config=db_config)
        self.logged_in_user = None  # تعریف متغیر برای کاربر لاگین شده

    @staticmethod
    def validate_input(prompt: str, min_length: int, error_message: str):
        value = input(prompt)
        if len(value) < min_length:
            raise ValueError(error_message)
        return value


    def save(self, username: str, password: str, nationality_code: str) -> Response:
        user = User(username, password, nationality_code)
        result = self._db.save(user=user)
        if result:
            return Response("OK", 200, user, "Registration successful.")
        else:
            return Response("NOT_OK", 603, user, "Error in Saving")

    def login(self, username: str, password: str) -> Response:
        hash_pass = hash_password(password)
        user = self._db.get_by_username_password(username, hash_pass)
        if user is None:
            return Response("NOT_OK", 604, None, "User not Found")
        self.logged_in_user = user  # ذخیره کاربر لاگین شده
        return Response("OK", 200, user, "Login successful")

    def validate_login(self) -> bool:
        return self.logged_in_user is not None

    def logout(self) -> str:
        if self.logged_in_user:
            self.logged_in_user = None
            return "Logout successful."
        return "No user is currently logged in."

    def find(self, nationality_code) -> Response:
        user = User(nationality_code=nationality_code)
        result = self._db.get_by_nationality_code(user.nationality_code)
        if result:
            return Response("OK", 200, user, "User found")
        return Response("NOT_FOUND", 604, None, "User not found")

    def update(self, username: str, password: str) -> Response:
        user = User(username, password)
        result = self._db.get_by_username_password(user.username, hash_password(user.password))
        if result:
            return Response("OK", 200, user, "Update successful")
        return Response("NOT_FOUND", 604, None, "User not found")

    def delete(self, nationality_code: str) -> Response:
        user = User(nationality_code=nationality_code)
        result = self._db.get_by_nationality_code(user.nationality_code)
        if result:
            self._db.delete(user)  # فرض بر این است که متد delete در UserDB تعریف شده است
            return Response("OK", 200, user, "User deleted")
        return Response("NOT_FOUND", 604, None, "User not found")
