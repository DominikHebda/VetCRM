from Database.connection import create_connection

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
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
  
fetch_doctors()

def add_doctor(first_name, last_name, specialization):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO doctors (first_name, last_name, specialization)
            values (%s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, specialization))
            connection.commit()
            print(f"Lekarz {first_name} {last_name} został dodany.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania lekarza: {e}")

def add_doctor_data():
    first_name = input("Podaj imię lekarza: ")
    last_name = input("Podaj nazwisko lekarza: ")
    specialization = input("Podaj specjalizacje lekarza: ")

    # add_doctor(first_name, last_name, specialization)

# add_doctor_data()

def find_doctor():
    try:
        first_name = input("Podaj imię szukanego lekarza: ").strip()
        last_name = input("Podaj nazwisko szukanego lekarza: ").strip()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        results = cursor.fetchall()

        if results:
            print(f"Znaleziono {len(results)} lekarzy: ")
            for row in results:
                print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Specjalizacja: {row[3]}")
            return results
        else:
            print("Nie znaleziono lekarzy o podanych danych.")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# find_doctor()

def update_doctor():
    doctors = find_doctor()
    if not doctors:
        print("Nie znaleziono lekarza o podanych danych: ")
        return
    
    try:
        doctor_id = int(input("Podaj ID lekarza, którego dane chcesz zaktualizować: "))
        selected_doctor = None
        for doctor in doctors:
            if doctor[0] == doctor_id:
                selected_doctor = doctor
                break
        
        if not selected_doctor:
            print("Nie znaleziono lekarza o podanym ID.")
            return
        
        print(f"Wybrano lekarza: {selected_doctor[1]} {selected_doctor[2]} (ID: {selected_doctor[0]})")

        new_first_name = input(f"Podaj nowe imię klienta ({selected_doctor[1]}) (pozostaw puste, aby nie zmieniać): ")
        new_last_name = input(f"Podaj nowe nazwisko klienta ({selected_doctor[2]}) (pozostaw puste, aby nie zmieniać): ")
        new_specialization = input(f"Podaj nowy numer telefonu klienta ({selected_doctor[3]}) (pozostaw puste, aby nie zmieniać): ")

        # Jeśli użytkownik nie podał nowych danych, pozostawiamy stare wartości
        new_first_name = new_first_name or selected_doctor[1]
        new_last_name = new_last_name or selected_doctor[2]
        new_specialization = new_specialization or selected_doctor[3]

        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE doctors
        SET first_name = %s, last_name = %s, specialization = %s
        WHERE iddoctor = %s
        """
        cursor.execute(query, (new_first_name, new_last_name, new_specialization, selected_doctor[0]))
        connection.commit()
        print(f"Dane lekarza {selected_doctor[1]} {selected_doctor[2]} zostały zaktualizowane.")

        cursor.close()
        connection.close()

    except ValueError:
        print("Błąd: Podano nieprawidłowe ID.")
    except Exception as e:
        print(f"Błąd podczas aktualizowania danych lekarza")

update_doctor()