from Database.connection import create_connection
from datetime import datetime
from urllib.parse import unquote
from datetime import timedelta
from Database.operations_client import add_client
from Database.operations_pets import add_pet
import traceback
import pymysql
import logging


logging.basicConfig(level=logging.DEBUG)

def get_current_time():
    return datetime.now()

# ############      FUNKCJA OBECNIE NIE UŻYWANA     #######################

def format_visit_time(visit_time):
    # Zakładam, że visit_time to obiekt datetime.timedelta
    hours = visit_time.seconds // 3600  # Pobieramy godziny
    minutes = (visit_time.seconds % 3600) // 60  # Pobieramy minuty
    return f"{hours:02}:{minutes:02}"  # Formatujemy jako HH:MM

# ##########################################################################

def fetch_visits():
    """Pobiera wszystkie wizyty z tabeli 'appointments'"""
    visits = []
    try:
        connection = create_connection()
        print("Połączenie z bazą danych nawiązane.")  # Debugowanie
        if connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT appointments.id, appointments.created_at, appointments.client_id, appointments.pet_id, appointments.doctor_id,
                          appointments.visit_date, appointments.visit_time, appointments.diagnosis, appointments.soft_delete,
                          clients.first_name AS client_first_name, clients.last_name AS client_last_name,
                          pets.pet_name AS pet_name, doctors.first_name AS doctor_first_name, doctors.last_name AS doctor_last_name
                   FROM appointments
                   JOIN clients ON appointments.client_id = clients.id
                   JOIN pets ON appointments.pet_id = pets.id
                   JOIN doctors ON appointments.doctor_id = doctors.id
                   ORDER BY appointments.visit_date DESC;''')

            results = cursor.fetchall()  # Pobiera wszystkie wyniki

            print("Dane pobrane z bazy:")  # Debugowanie
            for row in results:
                # Zastosowanie funkcji do przekształcenia timedelty na godziny i minuty
                visit_time_str = format_visit_time(row[6])  # row[6] to prawdopodobnie `visit_time`

                print(f"Data wizyty: {row[5]}, Czas wizyty: {visit_time_str}, Diagnoza: {row[7]}")  # Debugowanie

                # Zapisujemy dane wizyty w formie krotki (id, created_at, ...)
                visits.append({
                    'id': row[0],
                    'created_at': row[1],
                    'visit_date': row[5],
                    'visit_time': visit_time_str,
                    'diagnosis': row[7] if row[7] else "Brak diagnozy",
                    'soft_delete': row[8],
                    'client_full_name': f"{row[9]} {row[10]}",
                    'pet_name': row[11],
                    'doctor_full_name': f"{row[12]} {row[13]}"
                })

            
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return visits  # Zwraca listę wizyt


def find_visit_by_id(visit_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = '''
            SELECT id, created_at, client_id, pet_id, doctor_id, visit_date, visit_time, diagnosis
            FROM appointments
            WHERE id = %s AND soft_delete IS NULL
        '''
        cursor.execute(query, (visit_id,))
        result = cursor.fetchone()

        conn.close()

        return result  # np. (8, datetime.datetime(...), 1, 2, 3, date(...), '13:50', 'Brak diagnozy')

    except Exception as e:
        print(f"[BŁĄD] Nie udało się znaleźć wizyty o ID {visit_id}: {e}")
        return None




# fetch_scheduled_visits()

# POBIERANIE ID DOKTORA
def get_doctor_id(doctor_name):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT id FROM doctors WHERE last_name = %s"
            cursor.execute(query, (doctor_name,))
            result = cursor.fetchone()
            
            if result:
                return result[0] 
            else:
                print(f"Brak lekarza o nazwisku {doctor_name} w bazie danych.")
                return None 
    except Exception as e:
        print(f"Błąd podczas pobierania doctor_id: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None  

# POBIERANIE ID KLIENTA
def get_client_id(client_name):
    connection = None
    cursor = None
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            print("Połączenie z bazą danych zostało nawiązane.")
            
            query = "SELECT id FROM clients WHERE last_name = %s"
            cursor.execute(query, (client_name,))
            result = cursor.fetchone()
            
            if result:
                return result[0]  # Zwróć identyfikator klienta
            else:
                print(f"Brak klienta o nazwisku {client_name} w bazie danych.")
                return None 

    except Exception as e:
        print(f"Błąd podczas pobierania client_id: {e}")
        print("Szczegóły błędu:", traceback.format_exc())  # Wyświetlanie pełnego śladu błędu
    finally:
        # Bezpieczne zamknięcie kursora i połączenia
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"Błąd podczas zamykania kursora: {e}")
        if connection:
            try:
                if connection.is_connected():
                    connection.close()
                    print("Połączenie z bazą danych zostało zamknięte.")
            except Exception as e:
                print(f"Błąd podczas zamykania połączenia z bazą danych: {e}")
    
    return None  # Jeśli nie udało się pobrać identyfikatora

# POBIERAMYY DANE CLIENTA PO JEGO client_id
def get_client_data_by_id(client_id):
    """Pobierz dane klienta na podstawie jego ID."""
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM clients WHERE id = %s"
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()

        if result:
            return result  # Zwróć dane klienta (tuple)
        else:
            print(f"Brak klienta o ID {client_id} w bazie danych.")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania danych klienta: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return None


# POBIERANIE ID ZWIERZĘCIA
def get_pet_id(pet_name, client_id):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT id FROM pets WHERE pet_name = %s AND client_id = %s"
            cursor.execute(query, (pet_name, client_id))
            result = cursor.fetchone()
            
            if result:
                return result[0]  # Zwróć ID zwierzęcia
            else:
                return None
    except Exception as e:
        print(f"Błąd podczas pobierania pet_id: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None



# DODAWANIE NOWEJ/NASTĘPNEJ WIZYTY PRZEZ RECEPCJONISTKĘ
def add_next_visit(current_time, last_name_client, pet_name, doctor, date_of_visit, visit_time, first_name, phone, address, species, breed, age):
    print(f"species: {species}, breed: {breed}, age: {age}")

    connection = None
    cursor = None
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            print("Połączenie z bazą danych zostało nawiązane.")
            
            # Sprawdzamy, czy klient istnieje
            client_id = get_client_id(last_name_client)
            if client_id is None:
                print(f"Brak klienta o nazwisku {last_name_client} w bazie danych. Dodaję nowego klienta...")
                add_client(first_name, last_name_client, phone, address)
                client_id = get_client_id(last_name_client)
                if client_id is None:
                    print("Nie udało się znaleźć identyfikatora klienta. Wizyta nie zostanie zapisana.")
                    return

            doctor_id = get_doctor_id(doctor)
            if doctor_id is None:
                print(f"Nie udało się znaleźć identyfikatora lekarza {doctor}. Wizyta nie zostanie zapisana.")
                return

            # Dodajemy zwierzę do bazy danych, jeśli nie ma go jeszcze
            pet_id = get_pet_id(pet_name, client_id)
            if pet_id is None:
                print(f"Brak zwierzęcia {pet_name} w bazie danych. Dodaję nowe zwierzę...")
                add_pet(pet_name, species, breed, age, client_id)
                pet_id = get_pet_id(pet_name, client_id)
                if pet_id is None:
                    print("Nie udało się znaleźć identyfikatora zwierzęcia. Wizyta nie zostanie zapisana.")
                    return

            # Formatowanie daty wizyty
            date_of_visit = datetime.strptime(date_of_visit, "%Y-%m-%d").date()
            formatted_date_of_visit = date_of_visit.strftime("%Y-%m-%d")

            # Usuwamy mikrosekundy z current_time
            current_time = current_time.replace(microsecond=0)
            
            # Przypisanie zapytania SQL do zapisania wizyty
            query = """
            INSERT INTO appointments_made (date, last_name_client, pet_name, doctor, date_of_visit, doctor_id, client_id, visit_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            print(f"Zapytanie: {query} z wartościami: {current_time}, {last_name_client}, {pet_name}, {doctor}, {formatted_date_of_visit}, {doctor_id}, {client_id}, {visit_time}")

            cursor.execute(query, (current_time, last_name_client, pet_name, doctor, formatted_date_of_visit, doctor_id, client_id, visit_time))

            # Zatwierdzanie wizyty
            print(f"Zatwierdzam wizytę: {current_time}, {last_name_client}, {pet_name}, {doctor}, {visit_time}")
            connection.commit()
            print("Wizyta została zapisana.")
            cursor.close()
            connection.close()
            return True
            
        else:
            print("Brak połączenia z bazą danych.")
            return "Wystąpił błąd w połączeniu z bazą danych", 500

    except pymysql.MySQLError as e:
        print(f"Błąd MySQL: {e}")
        print("Szczegóły błędu:", traceback.format_exc())
        return "Błąd w bazie danych", 500
    except Exception as e:
        print(f"Błąd podczas zapisywania wizyty: {e}")
        print("Szczegóły błędu:", traceback.format_exc())
        return "Wystąpił błąd podczas zapisywania wizyty", 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            try:
                if connection.is_connected():
                    connection.close()
                    print("Połączenie z bazą danych zostało zamknięte.")
            except Exception as e:
                print(f"Błąd podczas zamykania połączenia z bazą danych: {e}")


def add_visit_data():
    last_name_client = input("Podaj nazwisko klienta: ")
    pet_name = input("Podaj nazwę zwierzęcia: ")
    doctor = input("Podaj nazwisko lekarza u którego odbędzie się ta wizyta: ")
    date_of_visit = input("Podaj datę planowanej wizyty (RRRR-MM-DD): ")

    # add_next_visit(datetime.now(), last_name_client, pet_name, doctor, date_of_visit)

# add_visit_data()

# DODAWANIE DIAGNOZY PRZEZ LEKARZA
def add_diagnosis(pet_name, doctor, diagnosis, current_time, date_of_next_visit):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            doctor_id = get_doctor_id(doctor)
            if doctor_id is None:
                print("Nie udało się znaleźć identyfikatora lekarza. Wizyta nie zostanie zapisana.")
                return
            date_of_next_visit = datetime.strptime(date_of_next_visit, "%Y-%m-%d").date()
            current_time = current_time or datetime.now()

            query = """
            INSERT INTO diagnoses (pet_name, doctor, diagnosis, diagnosis_date, date_of_next_visit, doctor_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (pet_name, doctor, diagnosis, current_time, date_of_next_visit, doctor_id))
            connection.commit()
            print("Diagnoza została zapisana.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas zapisywania wizyty: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_diagnosis_data():
    pet_name = input("Podaj nazwę zwierzęcia: ")
    doctor = input("Podaj nazwisko lekarza: ")
    diagnosis = input("Podaj diagnozę: ")
    date_of_next_visit = input("Podaj datę następnej wizyty (RRRR-MM-DD): ")

    # add_diagnosis(pet_name, doctor, diagnosis, datetime.now(), date_of_next_visit)

# add_diagnosis_data()

# WYSZUKANIE UMÓWIONEJ WIZYTY KLIENTOWI
def find_next_visit():
    try:
        last_name_client = input("Podaj nazwisko klienta: ")
        pet_name = input("Podaj nazwę zwierzęcia: ")
        doctor = input("Podaj nazwisko lekarza: ")
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT * FROM appointments_made
            WHERE (last_name_client = %s AND pet_name = %s) OR doctor = %s 
            """
            cursor.execute(query, (last_name_client, pet_name, doctor))
            result = cursor.fetchall()

            if result:
                print(f"Znaleziono {len(result)} wizyt:")
                for row in result:
                    print(f"Nazwisko klienta: {row[2]}, "
                          f"Nazwa zwierzęcia: {row[3]}, "
                          f"Nazwisko lekarza przyjmującego: {row[4]}, "
                          f"Data umówionej wizyty: {row[5]}")
                return result
            else:
                print("Brak wizyt na podane dane.")
                return None
    except Exception as e:
        print(f"Błąd podczas wyszukiwania wizyt: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# find_next_visit()

# UAKTUALNIANIE UMÓWIONEJ WIZYTY
def update_next_visit():
    try:
        visit_id = int(input("Podaj ID wizyty której dane chcesz zaktualizować: "))
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM appointments_made WHERE idappointments = %s", (visit_id,))
            result = cursor.fetchone()

            if result: 
                print(f"Znaleziono wizytę o podanym ID: {result}")
                selected_visit = result 

                new_last_name_client = input(f"Podaj nowe nazwisko klienta ({selected_visit[2]}) (pozostaw puste, aby nie zmieniać): ")
                new_pet_name = input(f"Podaj nową nazwę zwierzęcia ({selected_visit[3]}) (pozostaw puste, aby nie zmieniać): ")
                new_doctor = input(f"Podaj nowe nazwisko lekarza ({selected_visit[4]}) (pozostaw puste, aby nie zmieniać): ")
                new_date_visit = input(f"Podaj nową datę wizyty ({selected_visit[5]}) (pozostaw puste, aby nie zmieniać): ")

                new_last_name_client = new_last_name_client or selected_visit[2]
                new_pet_name = new_pet_name or selected_visit[3]
                new_doctor = new_doctor or selected_visit[4]
                new_date_visit = new_date_visit or selected_visit[5]

                cursor.execute("""
                UPDATE appointments_made
                SET last_name_client = %s, pet_name = %s, doctor = %s, date_of_visit = %s
                WHERE idappointments = %s
                """, (new_last_name_client, new_pet_name, new_doctor, new_date_visit, visit_id))

                connection.commit()
                print(f"Dane wizyty o ID {visit_id} zostały zaktualizowane.")
            else:
                print(f"Nie znaleziono wizyty o ID {visit_id}.")
            
            cursor.close()
            connection.close()
    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych wizyty: {e}")

# update_next_visit()

# UAKTUALNIANIE DIAGNOZY
def update_diagnosis():
    try:
        diagnosis_id = int(input("Podaj ID diagnozy której dane chcesz zaktualizować: "))
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM diagnoses WHERE iddiagnosis = %s", (diagnosis_id,))
            result = cursor.fetchone()

            if result: 
                print(f"Znaleziono wizytę o podanym ID: {result}")
                selected_diagnosis = result 

                new_pet_name = input(f"Podaj nową nazwę zwierzęcia ({selected_diagnosis[1]}) (pozostaw puste, aby nie zmieniać): ")
                new_doctor = input(f"Podaj nowe nazwisko lekarza ({selected_diagnosis[2]}) (pozostaw puste, aby nie zmieniać): ")
                new_diagnosis = input(f"Podaj nową diagnozę ({selected_diagnosis[3]}) (pozostaw puste, aby nie zmieniać): ")

                new_pet_name = new_pet_name or selected_diagnosis[1]
                new_doctor = new_doctor or selected_diagnosis[2]
                new_diagnosis = new_diagnosis or selected_diagnosis[3]

                cursor.execute("""
                UPDATE diagnoses
                SET  pet_name = %s, doctor = %s, diagnosis = %s
                WHERE iddiagnosis = %s
                """, (new_pet_name, new_doctor, new_diagnosis, diagnosis_id))

                connection.commit()
                print(f"Dane wizyty o ID {diagnosis_id} zostały zaktualizowane.")
            else:
                print(f"Nie znaleziono wizyty o ID {diagnosis_id}.")
            
            cursor.close()
            connection.close()
    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych wizyty: {e}")

# update_diagnosis()

# USUWANIE UMÓWIONEJ WIZYTY
def soft_delete_next_visit():
    visit_id = int(input("Podaj ID wizyty którą chcesz usunąć (soft delete): "))
    
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM appointments_made WHERE idappointments = %s", (visit_id,))
    selected_visit = cursor.fetchone()

    if not selected_visit:
        print(f"Nie znaleziono wizyty o Id {visit_id}.")
        return

    print(f"Wybrano wizytę: {selected_visit[2]} {selected_visit[3]} (ID: {selected_visit[0]})")

    current_time = datetime.now()

    query = """
    UPDATE appointments_made
    SET soft_delete = %s
    WHERE idvisits = %s AND soft_delete IS NULL
    """
    cursor.execute(query, (current_time, visit_id))
    connection.commit()

    if cursor.rowcount > 0:
        print(f"Wizyta o ID {visit_id} została oznaczona jako usunięta.")
    else:
        print(f"Nie udało się oznaczyć wizyty o ID {visit_id} jako usuniętej.")
    
    cursor.close()
    connection.close()

# soft_delete_next_visit()

def fetch_visits_details(visit_id):
    print(f"Fetching details for visit ID: {visit_id}")
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM appointments_made WHERE idappointments = %s"
            cursor.execute(query, (visit_id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Błąd podczas pobierania idappointments: {e}")
    finally: 
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None

def format_visit_time(visit_time):
    if isinstance(visit_time, timedelta):
        hours = visit_time.seconds // 3600 
        minutes = (visit_time.seconds % 3600) // 60 
        return f"{hours:02}:{minutes:02}"

    elif isinstance(visit_time, (int, float)):
        hours = visit_time // 3600  
        minutes = (visit_time % 3600) // 60  
        return f"{int(hours):02}:{int(minutes):02}"

    elif isinstance(visit_time, str) and len(visit_time) > 5:
        return visit_time[:5]

    return visit_time


def update_visit_in_db(visit_id, current_date_time, client_last_name, pet_name, doctor_name, date_of_visit, visit_time):
    try:
        client_last_name = unquote(client_last_name)
        pet_name = unquote(pet_name)
        doctor_name = unquote(doctor_name)

        visit_time = unquote(visit_time)

        if visit_time.count(":") == 2:
            visit_time = visit_time[:5] 

        if not visit_time:
            visit_time = fetch_visits_details(visit_id)[5].strftime('%H:%M:%S')  

        if visit_time.count(':') == 1:
            visit_time += ":00"

        full_date_time = f"{date_of_visit} {visit_time}"

        full_date_time = datetime.strptime(full_date_time, '%Y-%m-%d %H:%M:%S')

        print(f"Before update - client_last_name: {client_last_name}, pet_name: {pet_name}, doctor_name: {doctor_name}, visit_time: {visit_time}")

        current_date_time = datetime.now()

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SET NAMES 'utf8mb4'")
            cursor.execute(""" 
            UPDATE appointments_made 
            SET date = %s, last_name_client = %s, pet_name = %s, doctor = %s, date_of_visit = %s, visit_time = %s
            WHERE idappointments = %s
            """, (current_date_time, client_last_name, pet_name, doctor_name, full_date_time, visit_time, visit_id))
            
            connection.commit()
            return True
    except Exception as e:
        print(f"Błąd podczas aktualizacji wizyty: {e}")
    finally: 
        if connection.is_connected():
            cursor.close()
            connection.close()
    return False


# ##############################        FUNKCJE POMOCNICZE DO DODAWANIA WIZYTY      ##########################################


def fetch_clients_to_visit():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, last_name FROM clients")
        return cursor.fetchall()
    except Exception as e:
        print(f"Błąd podczas pobierania klientów: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_pets_to_visit(client_id):
    try:
        print(f"fetch_pets_to_visit: client_id = {client_id}")
        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT id, pet_name FROM pets WHERE client_id = %s"
        cursor.execute(query, (client_id,))
        results = cursor.fetchall()
        print(f"Liczba zwierząt klienta {client_id}: {len(results)}")
        return results
    except Exception as e:
        print(f"Błąd podczas pobierania zwierząt klienta {client_id}: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




def fetch_doctors_to_visit():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, last_name FROM doctors")
        return cursor.fetchall()
    except Exception as e:
        print(f"Błąd podczas pobierania lekarzy: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def add_visit(client_id, pet_id, doctor_id, visit_date, visit_time):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO appointments (client_id, pet_id, doctor_id, visit_date, visit_time)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (client_id, pet_id, doctor_id, visit_date, visit_time))
        connection.commit()
        print("Wizyta została zapisana.")
    except Exception as e:
        print(f"Błąd zapisu wizyty: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def find_visit(first_name, last_name, pet_name):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
        a.id,                                  -- ID wizyty
        p.pet_name,                            -- Imię zwierzęcia
        CONCAT(c.first_name, ' ', c.last_name) AS client_name,  -- Imię i nazwisko klienta
        a.visit_date,                          -- Data wizyty
        a.visit_time,                          -- Godzina wizyty
        a.diagnosis                            -- Diagnoza
    FROM appointments a
    JOIN clients c ON a.client_id = c.id
    JOIN pets p ON a.pet_id = p.id
    WHERE c.first_name = %s
      AND c.last_name = %s
      AND p.pet_name = %s
    ORDER BY a.visit_date DESC, a.visit_time DESC
    """

    cursor.execute(query, (first_name, last_name, pet_name))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

