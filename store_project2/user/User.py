import util.Utitilty
class User:
    def __init__(self, username: str, password: str, nationality_code: str, id: int = None):
        self.username = username
        self.password = util.Utitilty.hash_password(password)
        self.nationality_code = nationality_code
        self.id = id

    def __str__(self):
        return f"{self.username}, {self.nationality_code}"
