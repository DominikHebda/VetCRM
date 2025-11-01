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
                visit_time_str = format_visit_time(row[6])  # row[6] to `visit_time`

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


def update_visit(id, client_id, pet_id, doctor_id, visit_date, visit_time):
    
    try:# Połączenie z bazą
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SET NAMES 'utf8mb4'")

        # Aktualizacja po ID
        cursor.execute(""" 
            UPDATE appointments 
            SET 
                client_id = %s, 
                pet_id = %s, 
                doctor_id = %s, 
                visit_date = %s, 
                visit_time = %s
            WHERE id = %s
        """, (
            client_id,
            pet_id,
            doctor_id,
            visit_date,
            visit_time,
            id
        ))

        connection.commit()
        return True

    except Exception as e:
        print(f"Błąd podczas aktualizacji wizyty: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()




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


# #########         NOWY KOD POBIERANIA ZWIERZECIA          ###########

def fetch_pets_for_client(client_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, pet_name FROM pets 
        WHERE client_id = %s AND soft_delete IS NULL
    """, (client_id,))
    results = cursor.fetchall()
    conn.close()
    return results





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



# ###################           FUNKCJA DO /searching_visit/ AKTUALNA           ############################

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


def soft_delete_visit(visit_id):
    """
    Miękkie usunięcie wizyty (ustawia soft_delete na aktualną datę/czas).
    """
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SET NAMES 'utf8mb4'")

        current_time = datetime.now()

        # Oznaczenie wizyty jako usuniętej
        query = """
            UPDATE appointments
            SET soft_delete = NOW()
            WHERE id = %s
        """
        cursor.execute(query, [visit_id])

        connection.commit()
        return True

    except Exception as e:
        print(f"Błąd podczas usuwania wizyty: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def find_visits_by_client_id(client_id):
    """
    Zwraca listę wizyt (appointments) danego klienta.
    Każdy rekord: (pet_name, visit_date, visit_time, doctor_full_name, diagnosis)
    """
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                p.pet_name AS pet_name,
                a.visit_date,
                a.visit_time,
                CONCAT(d.first_name, ' ', d.last_name) AS doctor_full_name,
                a.diagnosis
            FROM appointments a
            JOIN pets p ON a.pet_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.client_id = %s
              AND (a.soft_delete IS NULL OR a.soft_delete = 0)
            ORDER BY a.visit_date DESC, a.visit_time DESC
        """
        cursor.execute(query, (client_id,))
        visits = cursor.fetchall()
        return visits

    except Exception as e:
        print(f"Błąd przy pobieraniu wizyt klienta: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def find_visits_by_doctor_id(doctor_id):
    """
    Zwraca listę wizyt danego lekarza.
    Każdy rekord: (pet_name, client_full_name, visit_date, visit_time, diagnosis)
    """
    connection = create_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                p.pet_name AS pet_name,
                CONCAT(c.first_name, ' ', c.last_name) AS client_full_name,
                a.visit_date,
                a.visit_time,
                a.diagnosis
            FROM appointments a
            JOIN pets p ON a.pet_id = p.id
            JOIN clients c ON a.client_id = c.id
            WHERE a.doctor_id = %s
              AND (a.soft_delete IS NULL OR a.soft_delete = 0)
            ORDER BY a.visit_date DESC, a.visit_time DESC
        """
        cursor.execute(query, (doctor_id,))
        visits = cursor.fetchall()
        return visits

    except Exception as e:
        print(f"Błąd przy pobieraniu wizyt lekarza: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
