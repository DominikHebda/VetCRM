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