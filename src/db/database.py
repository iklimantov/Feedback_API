import aiosqlite

# Путь к базе данных
DB_NAME = "src/db/database.sqlite"


async def get_connection():
    """Создаёт и возвращает асинхронное соединение с базой данных"""
    return await aiosqlite.connect(DB_NAME)
