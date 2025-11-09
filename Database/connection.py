import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.DEBUG)


def create_connection():
    """Tworzy połączenie z bazą danych MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin",
            database="vetcrm",
            port=3306
        )
        if connection.is_connected():
            logging.debug("Połączenie z bazą danych zostało nawiązane.")
            return connection
    except Error as e:
        logging.error(f"Błąd połączenia z bazą danych: {e}")
    return None