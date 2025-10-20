import aiosqlite
import random
from datetime import datetime, timedelta


DB_NAME = "database.sqlite"


# Инициализация и заполнение таблицы начальными данными.
async def init_db():
    """Создаёт базу данных и заполняет таблицы начальными данными"""

    async with aiosqlite.connect(DB_NAME) as conn:
        cursor = await conn.cursor()

        # Таблицы
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            subscribe BOOLEAN NOT NULL CHECK (subscribe IN (0, 1))
        )
        """)

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        # Данные пользователей
        users = {
            1: {'name': 'Vasia', 'email': 'vasia@example.com'},
            2: {'name': 'Peter Parker', 'email': 'peter.parker@example.com'},
            3: {'name': 'Tony Stark', 'email': 'tony.stark@example.com'},
            4: {'name': 'Natasha Romanoff', 'email': 'natasha.romanoff@example.com'},
            5: {'name': 'Bruce Wayne', 'email': 'bruce.wayne@example.com'},
            6: {'name': 'Clark Kent', 'email': 'clark.kent@example.com'},
            7: {'name': 'Diana Prince', 'email': 'diana.prince@example.com'},
            8: {'name': 'Barry Allen', 'email': 'barry.allen@example.com'},
            9: {'name': 'Stephen Strange', 'email': 'stephen.strange@example.com'},
            10: {'name': 'Wanda Maximoff', 'email': 'wanda.maximoff@example.com'}
        }

        for user in users.values():
            user["subscribe"] = random.choice([0, 1])

        # Очищаем таблицы
        await cursor.execute("DELETE FROM feedbacks")
        await cursor.execute("DELETE FROM users")

        # Добавляем пользователей
        for _, user in users.items():
            await cursor.execute(
                "INSERT INTO users (name, email, subscribe) VALUES (?, ?, ?)",
                (user["name"], user["email"], user["subscribe"])
            )

        await conn.commit()

        # Получаем ID всех пользователей
        await cursor.execute("SELECT id FROM users")
        rows = await cursor.fetchall()
        user_ids = [row[0] for row in rows]

        # Добавляем отзывы
        feedback_texts = [
            "Отличный сервис!", "Мне всё понравилось.", "Хотелось бы улучшить скорость ответа.",
            "Спасибо за помощь!", "Не работает форма обратной связи.", "Очень доволен качеством!",
            "Быстрая поддержка, рекомендую.", "Интерфейс можно сделать удобнее.",
            "Проблема решена, благодарю!", "Буду пользоваться снова."
        ]

        for user_id in user_ids:
            for _ in range(random.randint(1, 3)):
                text = random.choice(feedback_texts)
                date = datetime.now() - timedelta(
                    weeks=random.randint(0, 40),
                    days=random.randint(0, 6),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                await cursor.execute(
                    "INSERT INTO feedbacks (user_id, date, text) VALUES (?, ?, ?)",
                    (user_id, date.strftime("%Y-%m-%d %H:%M"), text)
                )

        await conn.commit()


# Для отладки — можно вызвать вручную:
# import asyncio
# asyncio.run(init_db())
