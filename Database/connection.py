import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.DEBUG)


def create_connection():
    """Tworzy połączenie z bazą danych MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",         # Adres hosta bazy danych
            user="root",  # Nazwa użytkownika
            password="Admin",   # Hasło do bazy danych
            database="vetcrm",         # Nazwa bazy danych
            port=3306 
        )
        
        if connection.is_connected():
            print("Połączenie z bazą danych zostało nawiązane.")
            return connection
        else:
            print("Nie udało się nawiązać połączenia z bazą danych.")
            return None

    except Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None
    
connection = create_connection()

if connection:
    # Kod do wykonywania operacji na bazie danych
    connection.close()
else:
    print("Połączenie z bazą danych nie udało się.")