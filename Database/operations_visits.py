from Database.connection import create_connection
from datetime import datetime

def fetch_visits():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM visits")
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

fetch_visits()

from datetime import datetime

def add_visits(pet_name, doctor, diagnosis, date_of_visit):
    try:
        connection = create_connection()
        if connection:
            current_time = datetime.now()
            cursor = connection.cursor()

            # Konwertujemy date_of_visit (string) na obiekt datetime.date
            date_of_visit = datetime.strptime(date_of_visit, "%Y-%m-%d").date()

            query = """
            INSERT INTO visits (date, pet_name, doctor, diagnosis, date_of_visit)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (current_time, pet_name, doctor, diagnosis, date_of_visit))
            connection.commit()
            print("Wizyta została zapisana.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas zapisywania wizyty: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_visits_data():
    pet_name = input("Podaj nazwę zwierzęcia: ")
    doctor = input("Podaj nazwisko lekarza u którego odbędzie się ta wizyta: ")
    diagnosis = input("Podaj diagnozę: ")
    date_of_visit = input("Podaj datę umówionej wizyty (RRRR-MM-DD): ")

    add_visits(pet_name, doctor, diagnosis, date_of_visit)

add_visits_data()



def find_visit():
    """Szukanie wizyty na podstawie daty i nazwy zwierzęcia."""
    try:
        # Zbieramy dane od użytkownika
        visit_date_input = input("Podaj datę szukanej wizyty (rrrr mm dd): ").strip()
        pet_name = input("Podaj nazwę zwierzęcia będącego na szukanej wizycie: ").strip()

        # Poprawiamy format daty, zmieniając ją na rrrr-mm-dd
        visit_date_parts = visit_date_input.split()
        if len(visit_date_parts) == 3:
            formatted_date = f"{visit_date_parts[0]}-{visit_date_parts[1]}-{visit_date_parts[2]}"
        else:
            print("Błąd formatu daty. Upewnij się, że podałeś datę w formacie rrrr mm dd.")
            return

        # Tworzymy połączenie z bazą danych
        connection = create_connection()
        cursor = connection.cursor()

        # Zapytanie SQL z parametrami
        query = """
        SELECT * FROM visits
        WHERE date = %s AND pet_name = %s
        """
        # Wykonanie zapytania z przekazaniem parametrów
        cursor.execute(query, (formatted_date, pet_name))

        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} wizyt:")
            for row in results:
                print(f"ID: {row[0]}, Data: {row[1]}, Nazwa zwierzęcia: {row[2]}, Nazwisko lekarza przyjmującego: {row[3]}, Diagnoza: {row[4]}")
        else:
            print("Nie znaleziono wizyt o podanych danych.")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")

find_visit()