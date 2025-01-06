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
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

fetch_scheduled_visits()

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
                print("Brak wizyt na podaną datę.")
                return None
    except Exception as e:
        print(f"Błąd podczas wyszukiwania wizyt: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

find_next_visit()


def update_visit():
    visits = find_next_visit()
    if not visits:
        return
    
    try:
        visit_id = int(input("Podaj ID wizyty której dane chcesz zaktualizować: "))
        selected_visit = None
        for visit in visits:
            if visit[0] == visit_id:
                selected_visit = visit
                break
        if not selected_visit:
            print("Nie znaleziono wizyty o podanym ID.")
            return
        
        print(f"Wybrano wizytę: {selected_visit[1]} {selected_visit[2]} (ID: {selected_visit[0]})")

        new_pet_name = input(f"Podaj nową nazwę zwierzęcia ({selected_visit[2]}) (pozostaw puste, aby nie zmieniać): ")
        new_doctor = input(f"Podaj nowe nazwisko lekarza({selected_visit[3]}) (pozostaw puste, aby nie zmieniać): ")
        new_diagnosis = input(f"Podaj nową diagnozę ({selected_visit[4]}) (pozostaw puste, aby nie zmieniać): ")

        # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
        new_pet_name = new_pet_name or selected_visit[2]
        new_doctor = new_doctor or selected_visit[3]
        new_diagnosis = new_diagnosis or selected_visit[4]

        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE visits
        SET pet_name = %s, doctor = %s, diagnosis = %s
        WHERE idvisit = %s
        """
        cursor.execute(query, (new_pet_name, new_doctor, new_diagnosis, visit_id))
        connection.commit()
        print(f"Dane wizyty {selected_visit[1]} {selected_visit[2]} zostały zaktualizowane.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych wizyty: {e}")

# update_visit()