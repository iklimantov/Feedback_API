import sqlite3


'''Чтение базы данных и вывод в консоль'''


DB_NAME = "database.sqlite"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("=== USERS ===")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

print("\n=== FEEDBACKS ===")
for row in cursor.execute("SELECT * FROM feedbacks"):
    print(row)

conn.close()
