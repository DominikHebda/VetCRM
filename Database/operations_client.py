from Database.connection import create_connection
from datetime import datetime
import traceback
import urllib.parse

# ######### KOD AKTUALNY - POTRZEBNA FUNKCJA ############
def fetch_clients():
    """Pobiera wszystkich klientów z tabeli 'clients'"""
    clients = []
    try:
        connection = create_connection()
        # print("Połączenie z bazą danych nawiązane.")  # Debugowanie
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, first_name, last_name, phone, address, soft_delete FROM clients")
            results = cursor.fetchall()  # Pobiera wszystkie wyniki

            # print("Dane pobrane z bazy:")  # Debugowanie
            for row in results:
                print(row)  # Debugowanie
                # Zapisujemy dane klienta w formie krotki (id, imię, nazwisko, telefon, adres)
                clients.append(row)
            
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return clients  # Zwraca listę klientów



# fetch_clients()


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
            # print(f"Adding client: {first_name}, {last_name}, {phone}, {address}") DEBUGOWANIE
            cursor.execute(query, (first_name, last_name, phone, address))
            connection.commit()
            # print(f"Klient {first_name} {last_name} został dodany.") DEBUGOWANIE
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania klienta: {e}")
        print(traceback.format_exc())
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ###############       STARY FRAGMENT KODU     ###############################

# def add_client_data():
#     """Pobiera dane klienta od użytkownika i dodaje go do bazy danych."""
#     first_name = input("Podaj imię klienta: ")
#     last_name = input("Podaj nazwisko klienta: ")
#     phone = input("Podaj numer telefonu klienta: ")
#     address = input("Podaj adres klienta: ")

    # add_client(first_name, last_name, phone, address)

# Wywołanie funkcji do dodania klienta po podaniu danych w konsoli
# add_client_data()

# #####################################################################################

# def add_client_and_pet_s(first_name, last_name, phone, address, pet_name, species, breed, age):
#     try:
#         connection = create_connection()
#         if connection:
#             cursor = connection.cursor()

#             # Zamiana '+' na spację w adresie
#             address = address.replace('+', ' ')

#             # Możemy również zastosować unquote, jeśli adres jest zakodowany w URL
#             address = urllib.parse.unquote(address)

#             query1 = """
#             INSERT INTO clients (first_name, last_name, phone, address)
#             VALUES (%s, %s, %s, %s)
#             """
#             query2 = """
#             INSERT INTO pets (pet_name, species, breed, age, client_id)
#             VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute("SET NAMES 'utf8mb4'")  # Ustawienie kodowania
#             print(f"Adding client: {first_name}, {last_name}, {phone}, {address}")
#             cursor.execute(query1, (first_name, last_name, phone, address))
            
#             # Uzyskujemy ID klienta po dodaniu klienta
#             client_id = cursor.lastrowid  # To jest autoinkrementowane ID ostatnio dodanego klienta

#             print(f"Adding pet: {pet_name}, {species}, {breed}, {age}")
#             cursor.execute(query2, (pet_name, species, breed, age, client_id))
#             connection.commit()
#             print(f"Klient {first_name} {last_name} oraz zwierzę {pet_name} zostały dodani.")
#             cursor.close()
#             connection.close()
#             return True  # Zwracamy True, aby wskazać sukces
#     except Exception as e:
#         print(f"Błąd podczas dodawania klienta: {e}")
#         print(traceback.format_exc())
#         return False  # Zwracamy False, jeśli wystąpił błąd
#     finally:
#         if connection and connection.is_connected():
#             cursor.close()
#             connection.close()


# SZUKANIE KLIENTÓW NA PODSTAWIE ID LUB IMIENIA I NAZWISKA
def find_client(first_name, last_name):
    """Szukanie klientów na podstawie imienia i nazwiska (ignorując spacje na początku/końcu)."""
    try:
        # Czyszczenie danych wejściowych z niechcianych spacji
        first_name = first_name.strip()
        last_name = last_name.strip()

        connection = create_connection()
        with connection.cursor() as cursor:
            print(f"Szukam klienta o imieniu: '{first_name}' i nazwisku: '{last_name}'")

            # TRIM usuwa spacje z początku i końca w bazie
            query = """
                SELECT * FROM clients
                WHERE TRIM(first_name) = TRIM(%s) AND TRIM(last_name) = TRIM(%s)
            """
            cursor.execute(query, (first_name, last_name))
            results = cursor.fetchall()

            if results:
                print(f"Znaleziono {len(results)} klient(a/ów):")
                for row in results:
                    print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Telefon: {row[3]}, Adres: {row[4]}")
                return results
            else:
                print("Nie znaleziono klientów o podanych danych.")
                return []

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None
    finally:
        if connection:
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


def soft_delete_client(client_id):
    """Oznacza klienta jako usuniętego w bazie danych (soft delete)"""
    try:
        # Tworzymy połączenie z bazą danych
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            # Pobieramy bieżącą datę i godzinę
            current_time = datetime.now()

            # Zapytanie SQL do oznaczenia klienta jako usuniętego
            query = """
            UPDATE clients
            SET soft_delete = %s
            WHERE id = %s AND soft_delete IS NULL
            """
            cursor.execute(query, (current_time, client_id))

            connection.commit()  # Zatwierdzamy zmiany w bazie danych

            # Sprawdzamy, czy zapytanie zaktualizowało jakikolwiek rekord
            if cursor.rowcount > 0:
                print(f"Klient o ID {client_id} został oznaczony jako usunięty.")
            else:
                print(f"Nie udało się oznaczyć klienta o ID {client_id} jako usuniętego.")
            
            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Błąd podczas oznaczania klienta jako usuniętego: {e}")