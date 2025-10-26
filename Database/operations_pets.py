from Database.connection import create_connection
from datetime import datetime

def fetch_pets():
    """Pobiera wszystkie zwierzęta z imieniem i nazwiskiem właściciela"""
    pets = []
    try:
        connection = create_connection()
        # print("Połączenie z bazą danych nawiązane.")
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.id, p.pet_name, p.species, p.breed, p.age, p.soft_delete,
                       c.first_name, c.last_name, c.id
                FROM pets p
                LEFT JOIN clients c ON p.client_id = c.id
            """)
            results = cursor.fetchall()
            # print("Dane pobrane z bazy:")
            for row in results:
                print(row)
                pets.append(row)
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return pets

# fetch_pets()

def add_pet(pet_name, species, breed, age, client_id):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO pets (pet_name, species, breed, age, client_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (pet_name, species, breed, age, client_id))
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

def fetch_clients_to_indications():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name FROM clients")
        return cursor.fetchall()
    except Exception as e:
        print(f"Błąd przy pobieraniu klientów: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def find_pet(pet_name, species):
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT p.id, p.pet_name, p.species, p.breed, p.age, p.soft_delete,
                   c.first_name, c.last_name, c.id
            FROM pets p
            JOIN clients c ON p.client_id = c.id
            WHERE p.pet_name = %s AND p.species = %s
        """, (pet_name, species))

        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} zwierząt:")
            for row in results:
                print(f"ID: {row[0]}, Nazwa: {row[1]}, Gatunek: {row[2]}, Rasa: {row[3]}")
            return results
        else:
            print("Nie znaleziono zwierząt o podanych danych.")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def find_pet_by_id(pet_id):
    """Znajduje Zwierzę po jego ID."""
    connection = create_connection()
    if connection is None:
        return None  # Jeśli połączenie się nie udało, zwracamy None

    try:
        cursor = connection.cursor()
        
        # Zapytanie SQL w celu znalezienia zwierzę po ID
        query = """SELECT p.id, p.pet_name, p.species, p.breed, p.age, p.client_id, c.first_name, c.last_name
                    FROM pets p
                    JOIN clients c ON p.client_id = c.id
                    WHERE p.id = %s
                    """
        cursor.execute(query, (pet_id,))
        
        # Pobranie jednego wyniku
        pet = cursor.fetchone()
        
        # Jeśli zwierzę istnieje, zwróć dane
        if pet:
            return pet  # Zwracamy krotkę (idPET, pet_name, species, breed, phone)
        else:
            return None  # Jeśli zwierzę nie został znaleziony

    except Exception as e:
        print(f"Błąd przy wyszukiwaniu zwierzęcia: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_pet(pet_id, pet_name, species, breed, age, client_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        print("Połączenie z bazą nawiązane.")

        pet_id = int(pet_id)

        query = """
        UPDATE pets
        SET pet_name = %s, species = %s, breed = %s, age = %s, client_id = %s
        WHERE id = %s
        """

        print(f"Zapytanie: {query}")
        print(f"Parametry: {(pet_name, species, breed, age, client_id, pet_id)}")

        cursor.execute(query, (pet_name, species, breed, age, client_id, pet_id))
        connection.commit()

        print(f"Dane zwierzęcia {pet_name} ({species}) zostały zaktualizowane.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych zwierzęcia: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def soft_delete_pet(pet_id):
    """Oznacza zwierzę jako usunięte w bazie danych (soft delete)"""
    try:
        # Tworzymy połączenie z bazą danych
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            # Pobieramy bieżącą datę i godzinę
            current_time = datetime.now()

            # Zapytanie SQL do oznaczenia zwierzęcia jako usuniętego
            query = """
            UPDATE pets
            SET soft_delete = %s
            WHERE id = %s AND soft_delete IS NULL
            """
            cursor.execute(query, (current_time, pet_id))

            connection.commit()  # Zatwierdzamy zmiany w bazie danych

            # Sprawdzamy, czy zapytanie zaktualizowało jakikolwiek rekord
            if cursor.rowcount > 0:
                print(f"Zwierzę o ID {pet_id} został oznaczony jako usunięty.")
            else:
                print(f"Nie udało się oznaczyć zwierzęcia o ID {pet_id} jako usuniętego.")
            
            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Błąd podczas oznaczania lekarza jako usuniętego: {e}")


# def update_pet():
#     pets = find_pet()
#     if not pets:
#         return
    
#     try:
#         pet_id = int(input("Podaj ID zwierzęcia, którego dane chcesz uaktualnić: "))
#         selected_pet = None
#         for pet in pets:
#             if pet[0] == pet_id:
#                 selected_pet = pet
#                 break
#         if not selected_pet:
#             print("Nie znaleziono zwierzęcia o podanym ID.")
#             return
#         print(f"Wybrano zwierzę: {selected_pet[1]} {selected_pet[2]} (ID: {selected_pet[0]})")

#         new_pet_name = input(f"Podaj nową nazwę zwierzęcia ({selected_pet[1]}) (pozostaw puste, aby nie zmieniać): ")
#         new_species = input(f"Podaj nowy gatunek zwierzęcia: ({selected_pet[2]}) (pozostaw puste, aby nie zmieniać): ")
#         new_breed = input(f"Podaj nową rasę zwierzęcia: ({selected_pet[3]}) (pozostaw puste, aby nie zmieniać): ")
#         new_age = input(f"Podaj nowy wiek zwierzęcia: ({selected_pet[4]}) (pozostaw puste, aby nie zmieniać): ")

#         # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
#         new_pet_name = new_pet_name or selected_pet[1]
#         new_species = new_species or selected_pet[2]
#         new_breed = new_breed or selected_pet[3]
#         new_age = new_age or selected_pet[4]

#         # Wykonujemy aktualizację
#         connection = create_connection()
#         cursor = connection.cursor()

#         query = """
#         UPDATE pets
#         SET pet_name = %s, species = %s, breed = %s, age = %s
#         WHERE idpet = %s
#         """
#         cursor.execute(query, (new_pet_name, new_species, new_breed, new_age, pet_id))
#         connection.commit()
#         print(f"Dane zwierzęcia {selected_pet[1]} {selected_pet[2]} zostały zaktualizowane.")

#         cursor.close()
#         connection.close()

#     except ValueError:
#         print("Błąd: Podano nieprawidłowe ID.")
#     except Exception as e:
#         print(f"Błąd podczas aktualizowania danych zwierzęcia: {e}")

# update_pet()