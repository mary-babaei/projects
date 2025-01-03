from buyer.buyer_db import BuyerDB
from config.config_service import get_config
from product.product_service import ProductService
from seller.seller_db import SellerDB
from user.user_service import UserService
from util.response import Response
from buyer.buyer_service import BuyerService
from seller.seller_service import SellerService

current_user = None

def validate_input(prompt: str, min_length: int, error_message: str) -> str:
    """Validate user input ensuring it meets minimum length requirements."""
    value = input(prompt)
    if len(value) < min_length:
        raise ValueError(error_message)
    return value


def read_file_and_write_in_db_buyer(config) -> None:
    """Read buyer data from a file and save it to the database."""
    service = BuyerService(config)

    print("Starting to read file and write data to DB for buyers.")
    with open(config.get("FILES", "BUYER_FILE"), "r") as f:
        for line in f:
            line = line.strip().split(",")
            if len(line) != 5:
                print(f"Invalid line skipped: {line}")
                continue
            try:
                service.save(line[0], line[1], line[2], line[3], line[4])
            except Exception as e:
                print(f"Error saving buyer: {str(e)}")

def create_product() -> Response:
    """Create a new product by a logged-in seller."""
    global current_user

    # Check if the seller is logged in
    if current_user is None:  # Verify that a user is logged in
        return Response("NOT_OK", 601, None, "You must be logged in to create a product.")

    try:
        name = validate_input("Enter Your Product Name: ", 5, "The Name does not meet strength requirements.")
        price = float(input("Enter Your Price: "))
        if price < 0:
            return Response("NOT_OK", 601, price, "The Price cannot be negative.")

        model = validate_input("Enter Your Product Model: ", 5, "The Model is not valid.")
        return ProductService.create_product(name, price, model, current_user)  # Use the current user to create product
    except ValueError as ve:
        return Response("NOT_OK", 601, None, str(ve))


def create_buyer(db_config) -> Response:
    try:
        username = validate_input("Enter Your Username: ", 5,
                                  "The Username does not meet strength requirements.")
        password = validate_input("Enter Your Password: ", 5,
                                  "The password does not meet strength requirements.")
        address = validate_input("Enter Your Address: ", 4, "The Address is not valid.")
        city = validate_input("Enter Your City: ", 3, "The City is not valid.")
        nationality_code = validate_input("Enter Your Nationality Code: ", 10,
                                          "The nationality code is not valid.")

        service = BuyerService(db_config)
        return service.save(username, password, nationality_code, address, city)
    except Exception as ex:
        return Response("NOT_OK", 601, None, str(ex))


def create_seller(db_config) -> Response:
    try:
        username = validate_input("Enter Your Username: ", 5,
                                  "The Username does not meet strength requirements.")
        password = validate_input("Enter Your Password: ", 5,
                                  "The password does not meet strength requirements.")
        shop_name = validate_input("Enter Your Shop Name: ", 4,
                                   "The Shop Name is not valid.")
        nationality_code = validate_input("Enter Your Nationality Code: ", 10,
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


current_user = None  # Global variable to track the current logged-in user

# Updating `login_user` to set current_user when login is successful
def login_user(db_config) -> Response:
    """Log in a user."""
    global current_user
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user_service = UserService(db_config=db_config)

    reaction = user_service.login(username, password)
    if reaction.status == "OK":
        current_user = reaction.data  # Store the user data upon successful login
        print(f"Welcome {username}!")
        return Response("ok", 200, reaction.data, "Login was successful")
    else:
        print("Login failed: ", reaction.message)
        return Response("not ok", 601, reaction.data, "Login was not successful.")


def signin_user(db_config) -> Response:
    """Sign in a new user."""
    global current_user

    username = validate_input("Enter your username: ", 5, "The Username does not meet requirements.")
    password = validate_input("Enter your password: ", 5, "The password does not meet requirements.")
    nationality_code = validate_input("Enter your nationality code: ", 10, "The nationality code is not valid.")

    user_service = UserService(db_config=db_config)
    reaction = user_service.save(username, password, nationality_code)

    if reaction.status == "OK":
        current_user = reaction.data  # Store user data upon successful sign-in
        print(f"Registration was successful for {username}!")
        return Response("ok", 200, reaction.data, "Registration was successful")
    else:
        print("Sign-up failed: ", reaction.message)
        return Response("not ok", 601, reaction.data, "Registration was not successful.")


# Initialize databases and settings
config = get_config("../config/config.ini")
startup = config.get("INITIAL", "startup")

if startup:
    BuyerDB(config).initial()
    SellerDB(config)

actions = {
    1: lambda: login_user(config),
    2: lambda: signin_user(config),
    3: lambda: create_buyer(config),
    4: lambda: create_seller(config),
    5: lambda: create_product(current_user),
    6: show_product_list,
    7: lambda: read_file_and_write_in_db_buyer(config),
}

print("\n\n««« Welcome to the Store Management System »»»")
while True:
    print("Available Actions:")
    print("1 - Login")
    print("2 - Sign-in")
    print("3 - Create Buyer")
    print("4 - Create Seller")
    print("5 - Create Product")
    print("6 - Show List of Products")
    print("7 - Load Buyers From File")
    print("8 - Exit")

    try:
        user_input = int(input("Enter Action #: "))
        if user_input in actions:
            response = actions[user_input]()
            if response:
                print(f"Response: {response}")
        elif user_input == 8:
            print("Exiting...")
            break
        else:
            print("Invalid action. Please try again.")
    except ValueError:
        print("Please Enter a valid number.")
    except KeyboardInterrupt:
        print("\nExiting program...")
        break
    finally:
        print("#" * 80)
