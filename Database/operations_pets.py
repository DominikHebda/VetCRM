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

    # add_pet(pet_name, species, breed, age)

# add_pet_data()

def find_pet():
    try:
        pet_name = input("Podaj nazwę zwierzęcia: ").strip()
        species = input("Podaj gatunek zwierzęcia: ").strip()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pets WHERE pet_name = %s AND species = %s", (pet_name, species))
        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} zwierząt:")
            for row in results:
                print(f"ID: {row[0]}, Nazwa zwierzęcia: {row[1]}, Gatunek: {row[2]} Rasa: {row[3]}")
            return results
        else:
            print("Nie znaleziono zwierząt o podanych danych.")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

find_pet()

def update_pet():
    pets = find_pet()
    if not pets:
        return
    
    try:
        pet_id = int(input("Podaj ID zwierzęcia, którego dane chcesz uaktualnić: "))
        selected_pet = None
        for pet in pets:
            if pet[0] == pet_id:
                selected_pet = pet
                break
        if not selected_pet:
            print("Nie znaleziono zwierzęcia o podanym ID.")
            return
        print(f"Wybrano zwierzę: {selected_pet[1]} {selected_pet[2]} (ID: {selected_pet[0]})")

        new_pet_name = input(f"Podaj nową nazwę zwierzęcia ({selected_pet[1]}) (pozostaw puste, aby nie zmieniać): ")
        new_species = input(f"Podaj nowy gatunek zwierzęcia: ({selected_pet[2]}) (pozostaw puste, aby nie zmieniać): ")
        new_breed = input(f"Podaj nową rasę zwierzęcia: ({selected_pet[3]}) (pozostaw puste, aby nie zmieniać): ")
        new_age = input(f"Podaj nowy wiek zwierzęcia: ({selected_pet[4]}) (pozostaw puste, aby nie zmieniać): ")

        # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
        new_pet_name = new_pet_name or selected_pet[1]
        new_species = new_species or selected_pet[2]
        new_breed = new_breed or selected_pet[3]
        new_age = new_age or selected_pet[4]

        # Wykonujemy aktualizację
        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE pets
        SET pet_name = %s, species = %s, breed = %s, age = %s
        WHERE idpet = %s
        """
        cursor.execute(query, (new_pet_name, new_species, new_breed, new_age, pet_id))
        connection.commit()
        print(f"Dane zwierzęcia {selected_pet[1]} {selected_pet[2]} zostały zaktualizowane.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych zwierzęcia: {e}")

update_pet()