from datetime import datetime
from Database.connection import create_connection

# POBIERANIE LISTY LEKARZY
def fetch_doctors():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM doctors")
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()
            connection.close()
            return results
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return []
  
# fetch_doctors()

def add_doctor(first_name, last_name, specialization, phone):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            query = """
            INSERT INTO doctors (first_name, last_name, specialization, phone)
            values (%s, %s, %s, %s)
            """
            cursor.execute("SET NAMES 'utf8mb4'")
            print(f"Adding doctor: {first_name}, {last_name}, {specialization}, {phone}")
            cursor.execute(query, (first_name, last_name, specialization, phone))
            connection.commit()
            print(f"Lekarz {first_name} {last_name} został dodany.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania lekarza: {e}")

# def add_doctor_data():
#     first_name = input("Podaj imię lekarza: ")
#     last_name = input("Podaj nazwisko lekarza: ")
#     specialization = input("Podaj specjalizacje lekarza: ")

#     add_doctor(first_name, last_name, specialization)

# add_doctor_data()





# SZUKANIE LEKARZY NA PODSTAWIE ID LUB IMIENIA I NAZWISKA
def find_doctor(first_name, last_name):
    """Szukanie lekarzy na podstawie imienia i nazwiska."""
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Logowanie przyjętych danych
        print(f"Szukam lekarza o imieniu: {first_name} i nazwisku: {last_name}")

        cursor.execute("SELECT * FROM doctors WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} lekarza:")
            for row in results:
                print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Specjalizacja: {row[3]}, Telefon: {row[4]}")
            return results  # Zwracamy listę wyników
        else:
            print("Nie znaleziono lekarza o podanych danych.")
            return None

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def find_doctor_by_id(doctor_id):
    """Znajduje lekarza po jego ID."""
    connection = create_connection()
    if connection is None:
        return None  # Jeśli połączenie się nie udało, zwracamy None

    try:
        cursor = connection.cursor()
        
        # Zapytanie SQL w celu znalezienia lekarza po ID
        query = "SELECT id, first_name, last_name, specialization, phone FROM doctors WHERE id = %s"
        cursor.execute(query, (doctor_id,))
        
        # Pobranie jednego wyniku
        doctor = cursor.fetchone()
        
        # Jeśli lekarz istnieje, zwróć dane
        if doctor:
            return doctor  # Zwracamy krotkę (idDoctor, first_name, last_name, specialization, phone)
        else:
            return None  # Jeśli lekarz nie został znaleziony

    except Exception as e:
        print(f"Błąd przy wyszukiwaniu lekarza: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_doctor(doctor_id, first_name, last_name, specialization, phone):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        print("Połączenie z bazą nawiązane.")

        doctor_id = int(doctor_id)

        query = """
        Update doctors
        SET first_name = %s, last_name = %s, specialization = %s, phone = %s
        WHERE id = %s
        """

        print(f"Wykonanie zapytania +: {query} z parametrami: {doctor_id}, {first_name}, {last_name}, {specialization}, {phone}")

        cursor.execute(query, (first_name, last_name, specialization, phone, doctor_id))
        connection.commit()

        print(f"Dane lekarza {first_name} {last_name} zostały zaktualizowane.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych lekarza: {e}")


def soft_delete_doctor(doctor_id):
    """Oznacza lekarza jako usuniętego w bazie danych (soft delete)"""
    try:
        # Tworzymy połączenie z bazą danych
        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            # Pobieramy bieżącą datę i godzinę
            current_time = datetime.now()

            # Zapytanie SQL do oznaczenia lekarza jako usuniętego
            query = """
            UPDATE doctors
            SET soft_delete = %s
            WHERE id = %s AND soft_delete IS NULL
            """
            cursor.execute(query, (current_time, doctor_id))

            connection.commit()  # Zatwierdzamy zmiany w bazie danych

            # Sprawdzamy, czy zapytanie zaktualizowało jakikolwiek rekord
            if cursor.rowcount > 0:
                print(f"Lekarz o ID {doctor_id} został oznaczony jako usunięty.")
            else:
                print(f"Nie udało się oznaczyć lekarza o ID {doctor_id} jako usuniętego.")
            
            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Błąd podczas oznaczania lekarza jako usuniętego: {e}")

# def update_doctor():
#     doctors = find_doctor()
#     if not doctors:
#         print("Nie znaleziono lekarza o podanych danych: ")
#         return
    
#     try:
#         doctor_id = int(input("Podaj ID lekarza, którego dane chcesz zaktualizować: "))
#         selected_doctor = None
#         for doctor in doctors:
#             if doctor[0] == doctor_id:
#                 selected_doctor = doctor
#                 break
        
#         if not selected_doctor:
#             print("Nie znaleziono lekarza o podanym ID.")
#             return
        
#         print(f"Wybrano lekarza: {selected_doctor[1]} {selected_doctor[2]} (ID: {selected_doctor[0]})")

#         new_first_name = input(f"Podaj nowe imię klienta ({selected_doctor[1]}) (pozostaw puste, aby nie zmieniać): ")
#         new_last_name = input(f"Podaj nowe nazwisko klienta ({selected_doctor[2]}) (pozostaw puste, aby nie zmieniać): ")
#         new_specialization = input(f"Podaj nowy numer telefonu klienta ({selected_doctor[3]}) (pozostaw puste, aby nie zmieniać): ")

#         # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
#         new_first_name = new_first_name or selected_doctor[1]
#         new_last_name = new_last_name or selected_doctor[2]
#         new_specialization = new_specialization or selected_doctor[3]

#         connection = create_connection()
#         cursor = connection.cursor()

#         query = """
#         UPDATE doctors
#         SET first_name = %s, last_name = %s, specialization = %s
#         WHERE iddoctor = %s
#         """
#         cursor.execute(query, (new_first_name, new_last_name, new_specialization, selected_doctor[0]))
#         connection.commit()
#         print(f"Dane lekarza {selected_doctor[1]} {selected_doctor[2]} zostały zaktualizowane.")

#         cursor.close()
#         connection.close()

#     except ValueError:
#         print("Błąd: Podano nieprawidłowe ID.")
#     except Exception as e:
#         print(f"Błąd podczas aktualizowania danych lekarza")

# update_doctor()