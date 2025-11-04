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


def update_pet(pet_id, pet_name, species, breed, age, new_client_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        pet_id = int(pet_id)
        new_client_id = int(new_client_id)

        # --- 1️⃣ Pobierz aktualnego właściciela (z tabeli pet_ownerships lub pets) ---
        cursor.execute("""
            SELECT client_id FROM pets WHERE id = %s
        """, (pet_id,))
        current_owner = cursor.fetchone()
        current_client_id = current_owner['client_id'] if current_owner else None

        # --- 2️⃣ Zaktualizuj dane zwierzęcia ---
        cursor.execute("""
            UPDATE pets
            SET pet_name = %s, species = %s, breed = %s, age = %s, client_id = %s
            WHERE id = %s
        """, (pet_name, species, breed, age, new_client_id, pet_id))

        # --- 3️⃣ Sprawdź, czy właściciel się zmienił ---
        if current_client_id != new_client_id:
            print(f"Zmieniono właściciela dla zwierzęcia ID {pet_id}: {current_client_id} → {new_client_id}")

            # 3a) Zakończ poprzedni rekord w pet_owner_history
            cursor.execute("""
                UPDATE pet_owner_history
                SET ownership_end = NOW(), active = 0
                WHERE pet_id = %s AND active = 1
            """, (pet_id,))

            # 3b) Dodaj nowy rekord z nowym właścicielem
            cursor.execute("""
                INSERT INTO pet_owner_history (pet_id, client_id, ownership_start, active)
                VALUES (%s, %s, NOW(), 1)
            """, (pet_id, new_client_id))

        connection.commit()
        print(f"✅ Dane zwierzęcia {pet_name} zostały zaktualizowane.")
        if current_client_id != new_client_id:
            print("Historia właścicieli została zaktualizowana.")

    except Exception as e:
        print(f"❌ Błąd podczas aktualizowania danych zwierzęcia: {e}")
        if connection:
            connection.rollback()
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

def find_pets_by_client_id(client_id):
    """
    Pobiera wszystkie zwierzęta należące do klienta o danym client_id z bazy MySQL.
    Zwraca listę krotek: (id, pet_name, species, breed, age, soft_delete)
    """
    # Połączenie z bazą danych – podmień parametry na swoje
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT id, pet_name, species, breed, age, soft_delete
    FROM pets
    WHERE client_id = %s
    ORDER BY id
    """
    
    cursor.execute(query, (client_id,))
    pets = cursor.fetchall()

    cursor.close()
    connection.close()
    return pets


def find_pet_details_by_id(pet_id):
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = """
            SELECT id, pet_name, species, breed, age, soft_delete, client_id
            FROM pets
            WHERE id = %s
        """
        cursor.execute(query, (pet_id,))
        pet = cursor.fetchone()
        return pet
    except Exception as e:
        print(f"Błąd przy pobieraniu zwierzęcia: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def fetch_pet_owner_history():
    """Pobiera historię zmian właścicieli zwierząt (relacja wiele-do-wielu)."""
    records = []
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                h.id,
                p.pet_name,
                CONCAT(c.first_name, ' ', c.last_name) AS owner_name,
                h.ownership_start,
                h.ownership_end,
                CASE WHEN h.active = 1 THEN 'Aktywna' ELSE 'Zakończona' END AS status
            FROM pet_owner_history h
            JOIN pets p ON h.pet_id = p.id
            JOIN clients c ON h.client_id = c.id
            ORDER BY h.ownership_start DESC;
        """)

        results = cursor.fetchall()
        for row in results:
            records.append(row)

    except Exception as e:
        print(f"Błąd podczas pobierania historii właścicieli: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return records

