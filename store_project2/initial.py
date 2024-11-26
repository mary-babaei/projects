
def create_table_users(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS products.TBL_USERS (
        id int primary key AUTO_INCREMENT,
        username nvarchar(50), 
        password nvarchar(20), 
        nationality_code varchar(10)
        )  
    '''
    connection.cursor().execute(query)
    print(f'Table product factors created successfully')

def create_table_seller(connection):
    query = """
    CREATE TABLE IF NOT EXISTS products.TBL_SELLERS (
    id int primary key AUTO_INCREMENT,
    shop_name nvarchar(100),
    shoping_id int,
    user_id  int,
    FOREIGN KEY (user_id) REFERENCES products.TBL_USERS(id))
    """
    connection.cursor().execute(query)
    print(f'Table seller created successfully')
    create_table_products(connection)


def create_table_products(connection):
    query = """
    CREATE TABLE IF NOT EXISTS products.TBL_PRODUCTS (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name NVARCHAR(100),
        price INTEGER,
        model NVARCHAR(100),
        seller_id INT,
        FOREIGN KEY (seller_id) REFERENCES products.TBL_SELLERS(id))
    """
    connection.cursor().execute(query)
    print(f'Table products created successfully')


def create_table_buyer(connection):
    query = """
        CREATE TABLE IF NOT EXISTS products.TBL_BUYERS (
        id int primary key AUTO_INCREMENT,
        address nvarchar(100),
        city nvarchar(100),
        buyer_id int,
        user_id  int,
        FOREIGN KEY (user_id) REFERENCES products.TBL_USERS(id))
        """
    connection.cursor().execute(query)
    print(f'Table buyer created successfully ')

def create_table_factor(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS products.TBL_PRODUCT_FACTORS (
        id int primary key AUTO_INCREMENT,
        seller_id INT,
        buyer_id INT,
        product_id INT,
        factor_id INT,
        date DATETIME,
        FOREIGN KEY (seller_id) REFERENCES products.TBL_SELLERS(id),
        FOREIGN KEY (buyer_id) REFERENCES products.TBL_BUYERS(id),
        FOREIGN KEY (product_id) REFERENCES products.TBL_PRODUCTS(id)
        )  
    '''
    connection.cursor().execute(query)
    print(f'Table product factors created successfully')