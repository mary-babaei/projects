from buyer.buyer_db import BuyerDB
from config.config_service import get_config
from product.product_service import ProductService
from seller.seller_db import SellerDB
from user.user_service import UserService
from util.response import Response
from buyer.buyer_service import BuyerService
from seller.seller_service import SellerService


class PanelCreate:
    def __init__(self, user_service: UserService):
        self.current_user = None
        self.config = get_config("../config/config.ini")
        self.user_service = user_service

    @staticmethod
    def validate_input(prompt: str, min_length: int, error_message: str):
        value = input(prompt)
        if len(value) < min_length:
            raise ValueError(error_message)
        return value


def validate_user_input(prompt: str, min_length: int, error_message: str) -> str:
    """Validate user input with a minimum length."""
    return PanelCreate.validate_input(prompt, min_length, error_message)


def create_product(current_user) -> Response:
    """Create a new product by a logged-in seller."""
    if not current_user or current_user.role != 'seller':
        return Response("NOT_OK", 601, None, "Only sellers can create products.")

    try:
        name = validate_user_input("Enter Your Product Name: ", 5, "The Name does not meet"
                                                                   " strength requirements.")
        price = float(input("Enter Your Price: "))
        if price < 0:
            return Response("NOT_OK", 601, price, "The Price cannot be negative.")

        model = validate_user_input("Enter Your Product Model: ", 5, "The Model is"
                                                                     " not valid.")
        return ProductService.create_product(name, price, model, current_user)
    except ValueError:
        return Response("NOT_OK", 601, None, "Invalid price entered.")

def create_buyer(db_config) -> Response:
    try:
        username = validate_user_input("Enter Your Username: ", 5, "The Username does not meet strength requirements.")
        password = validate_user_input("Enter Your Password: ", 5, "The password does not meet strength requirements.")
        address = validate_user_input("Enter Your Address: ", 4, "The Address is not valid.")
        city = validate_user_input("Enter Your City: ", 3, "The City is not valid.")
        nationality_code = validate_user_input("Enter Your Nationality Code: ", 10,
                                               "The nationality code is not valid.")

        service = BuyerService(db_config)
        return service.save(username, password, nationality_code, address, city)
    except Exception as ex:
        return Response("NOT_OK", 601, None, str(ex))


def create_seller(db_config) -> Response:
    try:
        username = validate_user_input("Enter Your Username: ", 5, "The Username does not meet strength requirements.")
        password = validate_user_input("Enter Your Password: ", 5, "The password does not meet strength requirements.")
        shop_name = validate_user_input("Enter Your Shop Name: ", 4, "The Shop Name is not valid.")
        nationality_code = validate_user_input("Enter Your Nationality Code: ", 10,
                                               "The nationality code is not valid.")

        service = SellerService(db_config)
        return service.save(username, password, nationality_code, shop_name)
    except Exception as ex:
        return Response("NOT_OK", 601, None, str(ex))

def show_product_list() -> None:
    """Display available products."""
    product_service = ProductService()
    products = product_service.read_all_products()
    if not products:
        print("No products available.")
    else:
        print("Available products:")
        for product in products:
            print(f"- {product.name}: {product.price} {product.currency}")


def login_user(db_config) -> Response:
    """Log in the user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user_service = UserService(db_config=db_config)

    reaction = user_service.login(username, password)
    if reaction.status == "OK":
        panel.current_user = reaction.data
        print(f"Welcome {panel.current_user.username}!")
        return Response("ok", 200, reaction, "login was successful")
    else:
        print("Login failed: ", reaction.message)
        return Response("not ok", 601, reaction, "login was not successful.")

def signin_user(db_config) -> Response:
    username = validate_user_input("Enter your username: ", 5, "The Username does not meet requirements.")
    password = validate_user_input("Enter your password: ", 5, "The password does not meet requirements.")
    nationality_code = input("Enter your nationality code: ")

    user_service = UserService(db_config=db_config)
    reaction = user_service.signin(username, password, nationality_code)

    if reaction.status == "OK":
        panel.current_user = reaction.data
        print(f"Registration was successful {panel.current_user.username}!")
        return Response("ok", 200, reaction, "Registration was successful")
    else:
        print("Signup failed: ", reaction.message)
        return Response("not ok", 601, reaction, "Registration was not successful.")


""" Initialize databases and settings """

config = get_config("../config/config.ini")
startup = config.get("INITIAL", "startup")

if startup:
    BuyerDB(config).initial()
    SellerDB(config)

panel = PanelCreate(UserService(db_config=config))

actions = {
    1: lambda: login_user(config),
    2: lambda: signin_user(config),
    3: lambda: create_buyer(config),
    4: lambda: create_seller(config),
    5: lambda: create_product(panel.current_user),
    6: show_product_list,
}

print("Welcome to the Store Management System")
while True:
    print("1 - Login")
    print("2 - Sign-in")
    print("3 - Create Buyer")
    print("4 - Create Seller")
    print("5 - Create Product")
    print("6 - Show List of Products")
    print("7 - Exit")

    try:
        user_input = int(input("Enter Action #: "))
        if user_input in actions:
            response = actions[user_input]()
            if response:
                print(f"Response: {response}")
        elif user_input == 7:
            print("Exiting...")
            break
        else:
            print("Invalid action. Please try again.")
    except ValueError:
        print("Enter a valid number.")
    except KeyboardInterrupt:
        print("\nExiting program...")
        break
    finally:
        print("#" * 50)
