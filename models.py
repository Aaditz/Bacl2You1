import uuid
from werkzeug.security import check_password_hash
from db import get_db_connection



# CREATE USER

def create_user(email, password):
    token = str(uuid.uuid4())

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO users (email, password, verified, verification_token) VALUES (?, ?, 0, ?)""",
        (email, password, token)
    )

    conn.commit()
    conn.close()

    return token

# CHECK USER EXISTS

def user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE email = ?",
        (email,)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists



# VERIFY USER (LOGIN)
# VERIFY USER (LOGIN)
def verify_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    if user["verified"] == 0:
        return "NOT_VERIFIED"

    if check_password_hash(user["password"], password):
        return user

    return None

