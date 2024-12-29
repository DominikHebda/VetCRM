from Database.connection import create_connection
from datetime import datetime

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

fetch_clients()


def add_client(first_name, last_name, phone, address):
    """Dodaje nowego klienta do tabeli customers."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO client (first_name, last_name, phone, address) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, phone, address))
            connection.commit()
            print("Klient został dodany.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania klienta: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_client_data():
    """Pobiera dane klienta od użytkownika i dodaje go do bazy danych."""
    first_name = input("Podaj imię klienta: ")
    last_name = input("Podaj nazwisko klienta: ")
    phone = input("Podaj numer telefonu klienta: ")
    address = input("Podaj adres klienta: ")

    add_client(first_name, last_name, phone, address)

# Wywołanie funkcji do dodania klienta po podaniu danych w konsoli
add_client_data()


def find_client():
    """Szukanie klientów na podstawie imienia i nazwiska."""
    try:
        first_name = input("Podaj imię szukanego klienta: ").strip()
        last_name = input("Podaj nazwisko szukanego klienta: ").strip()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM client WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} klientów:")
            for row in results:
                print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Telefon: {row[3]}, Adres: {row[4]}")
            return results  # Zwracamy listę wyników, aby można było je wykorzystać później
        else:
            print("Nie znaleziono klientów o podanych danych.")
            return None

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")


def update_client():
    """Aktualizuje dane klienta na podstawie ID."""
    # Szukamy klientów
    clients = find_client()
    if not clients:
        return  # Jeśli nie znaleziono żadnych klientów, kończymy działanie

    # Użytkownik wybiera ID klienta do aktualizacji
    try:
        # Pytamy użytkownika o ID klienta, którego chce zaktualizować
        client_id = int(input("Podaj ID klienta, którego dane chcesz zaktualizować: "))
        
        # Sprawdzamy, czy ID jest poprawne
        selected_client = None
        for client in clients:
            if client[0] == client_id:  # Zakładając, że ID klienta jest w pierwszej kolumnie
                selected_client = client
                break

        if not selected_client:
            print("Nie znaleziono klienta o podanym ID.")
            return

        print(f"Wybrano klienta: {selected_client[1]} {selected_client[2]} (ID: {selected_client[0]})")

        # Pobieramy dane, które chcemy zaktualizować
        new_first_name = input(f"Podaj nowe imię klienta ({selected_client[1]}) (pozostaw puste, aby nie zmieniać): ")
        new_last_name = input(f"Podaj nowe nazwisko klienta ({selected_client[2]}) (pozostaw puste, aby nie zmieniać): ")
        new_phone = input(f"Podaj nowy numer telefonu klienta ({selected_client[3]}) (pozostaw puste, aby nie zmieniać): ")
        new_address = input(f"Podaj nowy adres klienta ({selected_client[4]}) (pozostaw puste, aby nie zmieniać): ")

        # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
        new_first_name = new_first_name or selected_client[1]
        new_last_name = new_last_name or selected_client[2]
        new_phone = new_phone or selected_client[3]
        new_address = new_address or selected_client[4]

        # Wykonujemy aktualizację
        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE client
        SET first_name = %s, last_name = %s, phone = %s, address = %s
        WHERE idClient = %s
        """
        cursor.execute(query, (new_first_name, new_last_name, new_phone, new_address, client_id))
        connection.commit()
        print(f"Dane klienta {selected_client[1]} {selected_client[2]} zostały zaktualizowane.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych klienta: {e}")


# Wywołanie funkcji aktualizującej
update_client()


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

soft_delete_client()