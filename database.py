import sqlite3
import os

os.makedirs("data", exist_ok=True)

DB_NAME = "data/nova_ai.db"


def create_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_message(role, message):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO chats (role, message) VALUES (?, ?)",
        (role, message)
    )

    connection.commit()
    connection.close()


def get_chat_history():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT role, message FROM chats ORDER BY id"
    )

    history = [
        {"role": role, "content": message}
        for role, message in cursor.fetchall()
    ]

    connection.close()

    return history