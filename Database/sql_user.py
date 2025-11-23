from Database.connection import create_connection



def get_user_by_username(username):
    connection = create_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT password_hash, role, doctor_id FROM users WHERE username = %s",
            (username,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def insert_user(username, password_hash, full_name, role, doctor_id):
    conn = create_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, password_hash, full_name, role, doctor_id, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (username, password_hash, full_name, role, doctor_id))
        conn.commit()
        return True
    except Exception as e:
        print("SQL insert_user error:", e)
        return False
    finally:
        conn.close()