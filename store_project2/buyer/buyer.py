from user import User


class Buyer:
    def __init__(self, user: User, address, city, buyer_id):
        self.user = user
        self.address = address
        self.city = city
        self.buyer_id = buyer_id

    def __str__(self):
        return f'Username: {self.user.__str__()}, Address: {self.address}, City: {self.city}'
