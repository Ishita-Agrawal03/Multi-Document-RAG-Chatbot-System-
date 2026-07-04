import sqlite3

DB_PATH = "chatbot.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            filename TEXT,
            file_hash TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)

    conn.commit()
    conn.close()


def create_chat(title="New Chat"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chats(title)
        VALUES(?)
    """, (title,))

    conn.commit()

    chat_id = cursor.lastrowid

    conn.close()

    return chat_id


def get_all_chats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title
        FROM chats
        ORDER BY created_at DESC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats