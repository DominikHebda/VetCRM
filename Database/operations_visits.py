from Database.connection import create_connection
from datetime import datetime

def fetch_scheduled_visits():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM appointments_made")
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()
            return results
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# fetch_scheduled_visits()

# POBIERANIE ID DOKTORA
def get_doctor_id(doctor_name):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT iddoctor FROM doctors WHERE last_name = %s"
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

def get_client_id(client_name):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT idClient FROM client WHERE last_name = %s"
            cursor.execute(query, (client_name,))
            result = cursor.fetchone()
            
            if result:
                return result[0] 
            else:
                print(f"Brak klienta o nazwisku {client_name} w bazie danych.")
                return None 
    except Exception as e:
        print(f"Błąd podczas pobierania doctor_id: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None 

# DODAWANIE NOWEJ WIZYTY PRZEZ RECEPCJONISTKĘ
def add_next_visit(current_time, last_name_client, pet_name, doctor, date_of_visit): 
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            client_id = get_client_id(last_name_client)
            if client_id is None:
                print("Nie udało się znaleźć identyfikatora klienta. Wizyta nie zostanie zapisana.")
                return

            doctor_id = get_doctor_id(doctor)
            if doctor_id is None:
                print("Nie udało się znaleźć identyfikatora lekarza. Wizyta nie zostanie zapisana.")
                return

            date_of_visit = datetime.strptime(date_of_visit, "%Y-%m-%d").date()
            formatted_date_of_visit = date_of_visit.strftime("%Y-%m-%d")

            query = """
            INSERT INTO appointments_made (date, last_name_client, pet_name, doctor, date_of_visit, doctor_id, client_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (current_time, last_name_client, pet_name, doctor, formatted_date_of_visit, doctor_id, client_id))
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
            WHERE last_name_client = %s AND pet_name = %s OR doctor = %s 
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

def update_visit_in_db(visit_id, date, client_last_name, pet_name, doctor_name, date_of_visit):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            cursor.execute("""
            UPDATE appointments_made 
            SET date = %s, last_name_client = %s, pet_name = %s, doctor = %s, date_of_visit = %s 
            WHERE idappointments = %s
            """, (date, client_last_name, pet_name, doctor_name, date_of_visit, visit_id))
            
            connection.commit()
            return True
    except Exception as e:
        print(f"Błąd podczas aktualizacji wizyty: {e}")
    finally: 
        if connection.is_connected():
            cursor.close()
            connection.close()
    return False

