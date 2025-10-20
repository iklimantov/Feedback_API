import sqlite3


# Путь к базе данных
DB_NAME = "src/db/database.sqlite"


def get_connection():
    """Создаёт и возвращает соединение с базой данных"""
    return sqlite3.connect(DB_NAME)
