from database.DBConnector import DBConnector


def dbExecute(sql="", exType="", params=None):
    mysql_cursor = None
    mysql_connection = None
    try:
        db_connector = DBConnector()
        (mysql_connection, mysql_cursor) = db_connector.get_connection()
        if exType == "executemany":
            mysql_cursor.executemany(sql, params or [])
            mysql_connection.commit()
            return mysql_cursor.rowcount
        mysql_cursor.execute(sql, params or ())
        if exType == "fetchone":
            result = mysql_cursor.fetchone()
            return dict(result) if result else None
        if exType == "fetchall":
            return mysql_cursor.fetchall()
        mysql_connection.commit()
        if exType == "insert" and mysql_cursor.lastrowid:
            return mysql_cursor.lastrowid
        return mysql_cursor.rowcount
    except Exception as err:
        if mysql_connection:
            mysql_connection.rollback()
        raise err
    finally:
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_connection:
            mysql_connection.close()
