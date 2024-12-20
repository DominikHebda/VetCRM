import mysql.connector
from mysql.connector import Error

def create_connection():
    """Tworzy połączenie z bazą danych MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="twoje_uzytkownik",
            password="twoje_haslo",
            database="vetcrm"
        )
        if connection.is_connected():
            print("Połączenie z bazą danych zostało nawiązane.")
            return connection
    except Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None
