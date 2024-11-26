from user import User


class Seller:
    def __init__(self, shop_name, shoping_id, user: User, id:int = None):
        self.shop_name = shop_name
        self.shoping_id = shoping_id
        self.user = user
        self.id = id

    def __str__(self):
        return f"{self.user.__str__()} {self.shop_name} {self.shoping_id}"
