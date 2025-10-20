from fastapi import APIRouter, HTTPException
from src.db.database import get_connection
from src.models.schemas import UsersResponse, User, UserCreate, MessageResponse


router = APIRouter(prefix="/users", tags=["Users"])


# Получение списка всех пользователей из базы данных
@router.get("/", response_model=UsersResponse)
def get_users():
    """
    Получение списка всех пользователей
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, subscribe FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "subscribe": bool(row[3])
        }
        for row in rows
    ]
    return {"users": users}


# Добавление нового пользователя в базу данных
@router.post("/", response_model=User)
def add_user(user: UserCreate):
    """
    Добавляет нового пользователя в базу данных.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, email, subscribe)
        VALUES (?, ?, ?)
        """,
        (user.name, user.email, int(user.subscribe))
    )
    conn.commit()
    user_id = cursor.lastrowid  # id только что добавленного пользователя

    conn.close()
    return User(id=user_id, name=user.name, email=user.email, subscribe=user.subscribe)


# Удаление пользователя по id из базы данных
@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int):
    """
    Удаляет пользователя по id и возвращает сообщение с подтверждением.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Сначала получаем данные пользователя, чтобы вернуть после удаления
    cursor.execute("SELECT id, name, email, subscribe FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    deleted_user = User(id=row[0], name=row[1], email=row[2], subscribe=bool(row[3]))

    # Удаляем пользователя
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return {"message": f'Пользователь {deleted_user.name} с id {deleted_user.id} удален'}
