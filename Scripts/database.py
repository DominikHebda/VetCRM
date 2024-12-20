import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",       
            password="password",  
            database="vetcrm"  
        )
        if connection.is_connected():
            print("Połączenie z bazą danych zostało nawiązane!")
        return connection
    except Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Połączenie z bazą danych zostało zamknięte.")
