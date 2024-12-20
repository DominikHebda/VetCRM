from Database.db_connection import create_connection

def fetch_customers():
    """Pobiera wszystkich klientów z tabeli customers."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customers")
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")

def add_customer(first_name, last_name, phone, address):
    """Dodaje nowego klienta do tabeli customers."""
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO customers (first_name, last_name, phone, address) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, phone, address))
            connection.commit()
            print("Klient został dodany.")
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Błąd podczas dodawania klienta: {e}")
