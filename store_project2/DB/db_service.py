import mysql


class DBService:
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(
                        host=db_config.get('DATABASE', 'host'),
                        port=db_config.get('DATABASE', 'port'),
                        user=db_config.get('DATABASE', 'user'),
                        password=db_config.get('DATABASE', 'password'),
                    )
