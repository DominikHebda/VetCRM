from Database.connection import create_connection
from password_utils import hash_password

def add_user(username, password):
    conn = create_connection()
    if not conn:
        print("❌ Brak połączenia z bazą!")
        return

    cursor = conn.cursor()

    # Sprawdź, czy użytkownik już istnieje
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print(f"⚠️  Użytkownik '{username}' już istnieje!")
    else:
        password_hash = hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print(f"✅ Dodano użytkownika: {username}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    add_user("Admin", "Admin")

