import pymysql
from pymysql.cursors import DictCursor

from app.helpers.config import Config


class DBConnector:
    def get_connection(self):
        config = Config()
        return pymysql.connect(
            host=config.mysql_host,
            port=config.mysql_port,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database,
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False,
            connect_timeout=10,
        )
