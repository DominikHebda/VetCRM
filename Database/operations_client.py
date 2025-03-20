from Database.connection import create_connection
from Database.operations_pets import add_pet
from datetime import datetime
import traceback
import urllib.parse


def fetch_clients():
    """Pobiera wszystkich klientów z tabeli customers."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM client")
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

# fetch_clients()


import urllib.parse

def add_client(first_name, last_name, phone, address):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            # Zamiana '+' na spację w adresie
            address = address.replace('+', ' ')

            # Możemy również zastosować unquote, jeśli adres jest zakodowany w URL
            address = urllib.parse.unquote(address)

            query = """
            INSERT INTO clients (first_name, last_name, phone, address)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute("SET NAMES 'utf8mb4'")  # Ustawienie kodowania
            print(f"Adding client: {first_name}, {last_name}, {phone}, {address}")
            cursor.execute(query, (first_name, last_name, phone, address))
            connection.commit()
            print(f"Klient {first_name} {last_name} został dodany.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania klienta: {e}")
        print(traceback.format_exc())
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def add_client_data():
    """Pobiera dane klienta od użytkownika i dodaje go do bazy danych."""
    first_name = input("Podaj imię klienta: ")
    last_name = input("Podaj nazwisko klienta: ")
    phone = input("Podaj numer telefonu klienta: ")
    address = input("Podaj adres klienta: ")

    # add_client(first_name, last_name, phone, address)

# Wywołanie funkcji do dodania klienta po podaniu danych w konsoli
# add_client_data()

def add_client_and_pet_s(first_name, last_name, phone, address, pet_name, species, breed, age):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            # Zamiana '+' na spację w adresie
            address = address.replace('+', ' ')

            # Możemy również zastosować unquote, jeśli adres jest zakodowany w URL
            address = urllib.parse.unquote(address)

            query1 = """
            INSERT INTO clients (first_name, last_name, phone, address)
            VALUES (%s, %s, %s, %s)
            """
            query2 = """
            INSERT INTO pets (pet_name, species, breed, age, client_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute("SET NAMES 'utf8mb4'")  # Ustawienie kodowania
            print(f"Adding client: {first_name}, {last_name}, {phone}, {address}")
            cursor.execute(query1, (first_name, last_name, phone, address))
            
            # Uzyskujemy ID klienta po dodaniu klienta
            client_id = cursor.lastrowid  # To jest autoinkrementowane ID ostatnio dodanego klienta

            print(f"Adding pet: {pet_name}, {species}, {breed}, {age}")
            cursor.execute(query2, (pet_name, species, breed, age, client_id))
            connection.commit()
            print(f"Klient {first_name} {last_name} oraz zwierzę {pet_name} zostały dodani.")
            cursor.close()
            connection.close()
            return True  # Zwracamy True, aby wskazać sukces
    except Exception as e:
        print(f"Błąd podczas dodawania klienta: {e}")
        print(traceback.format_exc())
        return False  # Zwracamy False, jeśli wystąpił błąd
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# SZUKANIE KLIENTÓW NA PODSTAWIE ID LUB IMIENIA I NAZWISKA
def find_client(first_name, last_name):
    """Szukanie klientów na podstawie imienia i nazwiska."""
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Logowanie przyjętych danych
        print(f"Szukam klienta o imieniu: {first_name} i nazwisku: {last_name}")

        cursor.execute("SELECT * FROM clients WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} klienta:")
            for row in results:
                print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Telefon: {row[3]}, Adres: {row[4]}")
            return results  # Zwracamy listę wyników
        else:
            print("Nie znaleziono klientów o podanych danych.")
            return None

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def find_client_by_id(client_id):
    """Znajduje klienta po jego ID."""
    connection = create_connection()
    if connection is None:
        return None  # Jeśli połączenie się nie udało, zwracamy None

    try:
        cursor = connection.cursor()
        
        # Zapytanie SQL w celu znalezienia klienta po ID
        query = "SELECT id, first_name, last_name, phone, address FROM clients WHERE id = %s"
        cursor.execute(query, (client_id,))
        
        # Pobranie jednego wyniku
        client = cursor.fetchone()
        
        # Jeśli klient istnieje, zwróć dane
        if client:
            return client  # Zwracamy krotkę (idClient, first_name, last_name, phone, address)
        else:
            return None  # Jeśli klient nie został znaleziony

    except Exception as e:
        print(f"Błąd przy wyszukiwaniu klienta: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_client(client_id, first_name, last_name, phone, address):
    """Aktualizuje dane klienta na podstawie ID w aplikacji webowej."""
    try:
        connection = create_connection()  # Funkcja tworząca połączenie z bazą
        cursor = connection.cursor()

        print("Połączenie z bazą danych nawiązane.")  # Sprawdzenie połączenia

        # Upewnij się, że client_id jest liczbą, jeśli tego wymaga baza
        client_id = int(client_id)

        query = """
        UPDATE clients
        SET first_name = %s, last_name = %s, phone = %s, address = %s
        WHERE id = %s 
        """

        print(f"Wykonywane zapytanie: {query} z parametrami: {first_name}, {last_name}, {phone}, {address}, {client_id}")

        cursor.execute(query, (first_name, last_name, phone, address, client_id))
        connection.commit()

        print(f"Dane klienta {first_name} {last_name} zostały zaktualizowane.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych klienta: {e}")



# Wywołanie funkcji aktualizującej
# update_client()


def soft_delete_client():
    """Soft delete klienta na podstawie jego ID, po wcześniejszym wyszukaniu."""
    # Wyszukaj klientów
    clients = find_client()
    if not clients:
        return  # Jeśli nie znaleziono żadnych klientów, kończymy działanie

    try:
        # Pytamy użytkownika o ID klienta, którego chce usunąć
        client_id = int(input("Podaj ID klienta, którego chcesz usunąć (soft delete): "))

        # Sprawdzamy, czy klient o podanym ID istnieje w wynikach wyszukiwania
        selected_client = None
        for client in clients:
            if client[0] == client_id:  # Zakładając, że ID klienta jest w pierwszej kolumnie
                selected_client = client
                break

        if not selected_client:
            print(f"Nie znaleziono klienta o ID {client_id}.")
            return

        print(f"Wybrano klienta: {selected_client[1]} {selected_client[2]} (ID: {selected_client[0]})")

        # Pobieramy bieżącą datę i godzinę
        current_time = datetime.now()

        # Połączenie z bazą danych i wykonanie zapytania aktualizującego 
        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE client
        SET soft_delete = %s
        WHERE idClient = %s AND soft_delete IS NULL
        """
        cursor.execute(query, (current_time, client_id))
        connection.commit()

        # Sprawdzamy, czy rekord został zaktualizowany
        if cursor.rowcount > 0:
            print(f"Klient o ID {client_id} został oznaczony jako usunięty.")
        else:
            print(f"Nie udało się oznaczyć klienta o ID {client_id} jako usuniętego.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas oznaczania klienta jako usuniętego: {e}")

# soft_delete_client()