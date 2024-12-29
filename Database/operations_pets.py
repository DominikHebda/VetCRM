from Database.connection import create_connection
from datetime import datetime

def fetch_pets():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pets")
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

fetch_pets()

def add_pet(pet_name, species, breed, age):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO pets (pet_name, species, breed, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (pet_name, species, breed, age))
            connection.commit()
            print(f"Zwierzę {pet_name} zostało dodane")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania zwierzęcia {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_pet_data():
    pet_name = input("Podaj nazwę zwierzęcia: ")
    species = input("Podaj gatunek zawierzęcia: ")
    breed = input("Podaj rasę zwierzęcia: ")
    age = input("Podaj wiek zwierzęcia: ")

    add_pet(pet_name, species, breed, age)

add_pet_data()