import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "educator.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            intent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_titles (
            user_id INTEGER NOT NULL,
            conversation_id TEXT NOT NULL,
            title TEXT NOT NULL,
            PRIMARY KEY (user_id, conversation_id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(username: str, email: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password))
        )
        conn.commit()
        return True, "Account created successfully"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists"
        return False, "Email already exists"
    finally:
        conn.close()

def verify_user(username: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password"], password):
        return user
    return None

def save_message(user_id: int, conversation_id: str, role: str, message: str, intent: str = None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, conversation_id, role, message, intent) VALUES (?, ?, ?, ?, ?)",
        (user_id, conversation_id, role, message, intent)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id: int, conversation_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, message, intent, created_at FROM chat_history "
        "WHERE user_id = ? AND conversation_id = ? ORDER BY created_at ASC",
        (user_id, conversation_id)
    )
    history = cursor.fetchall()
    conn.close()
    return history

def get_latest_conversation_id(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT conversation_id FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row["conversation_id"] if row else None

def new_conversation_id() -> str:
    return str(uuid.uuid4())

def get_conversations(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            conversation_id,
            MAX(created_at) AS last_at,
            COALESCE(
                (SELECT t.title FROM conversation_titles t
                 WHERE t.user_id = ?
                   AND t.conversation_id = chat_history.conversation_id),
                (SELECT message FROM chat_history c2
                 WHERE c2.conversation_id = chat_history.conversation_id
                   AND c2.role = 'user'
                 ORDER BY c2.created_at ASC LIMIT 1)
            ) AS title
        FROM chat_history
        WHERE user_id = ?
        GROUP BY conversation_id
        ORDER BY last_at DESC
    """, (user_id, user_id))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_conversation(user_id: int, conversation_id: str) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM chat_history WHERE user_id = ? AND conversation_id = ?",
        (user_id, conversation_id)
    )
    deleted = cursor.rowcount
    cursor.execute(
        "DELETE FROM conversation_titles WHERE user_id = ? AND conversation_id = ?",
        (user_id, conversation_id)
    )
    conn.commit()
    conn.close()
    return deleted

def rename_conversation(user_id: int, conversation_id: str, title: str) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    # only rename chats that really belong to this user
    cursor.execute(
        "SELECT 1 FROM chat_history WHERE user_id = ? AND conversation_id = ? LIMIT 1",
        (user_id, conversation_id)
    )
    if not cursor.fetchone():
        conn.close()
        return False
    cursor.execute(
        "INSERT OR REPLACE INTO conversation_titles (user_id, conversation_id, title) VALUES (?, ?, ?)",
        (user_id, conversation_id, title)
    )
    conn.commit()
    conn.close()
    return True