from datetime import datetime
from Database.connection import create_connection


def add_receptionist(first_name, last_name):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            cursor.execute("SET NAMES 'utf8mb4'")

            query = """
            INSERT INTO receptionists (first_name, last_name)
            values (%s, %s)
            """

            cursor.execute(query, (first_name, last_name))
            connection.commit()
            print(f"Recepcjonistka {first_name} {last_name} została dodana.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania lekarza: {e}")
