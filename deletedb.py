import sqlite3
import os

DB_PATH = "instance/users.db"

def delete_all_users():
    # Safety check: DB file exists
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Delete all users
    cursor.execute("DELETE FROM users")

    # Reset auto-increment ID (SQLite)
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

    conn.commit()
    conn.close()

    print("✅ All users deleted successfully from users table")
    print("🔁 User ID counter reset to 1")

def verify_delete():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()
    print(f"📊 Current users count: {count}")

if __name__ == "__main__":
    print("⚠️ WARNING: This will DELETE ALL USERS from the database!")
    confirm = input("Type YES to continue: ")

    if confirm == "YES":
        delete_all_users()
        verify_delete()
    else:
        print("❌ Operation cancelled")
