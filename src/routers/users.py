from fastapi import APIRouter, HTTPException
from src.db.database import get_connection
from src.models.schemas import UsersResponse, User, UserCreate, MessageResponse

router = APIRouter(prefix="/users", tags=["Users"])


# Получение списка всех пользователей из базы данных
@router.get("/", response_model=UsersResponse)
async def get_users():
    """
    Получение списка всех пользователей
    """
    conn = await get_connection()
    cursor = await conn.execute("SELECT id, name, email, subscribe FROM users")
    rows = await cursor.fetchall()
    await conn.close()

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
async def add_user(user: UserCreate):
    """
    Добавляет нового пользователя в базу данных.
    """
    conn = await get_connection()
    await conn.execute(
        """
        INSERT INTO users (name, email, subscribe)
        VALUES (?, ?, ?)
        """,
        (user.name, user.email, int(user.subscribe))
    )
    await conn.commit()

    cursor = await conn.execute("SELECT last_insert_rowid()")
    user_id = (await cursor.fetchone())[0]
    await conn.close()

    return User(id=user_id, name=user.name, email=user.email, subscribe=user.subscribe)


# Удаление пользователя по id из базы данных
@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: int):
    """
    Удаляет пользователя по id и возвращает сообщение с подтверждением.
    """
    conn = await get_connection()

    cursor = await conn.execute("SELECT id, name, email, subscribe FROM users WHERE id = ?", (user_id,))
    row = await cursor.fetchone()
    if not row:
        await conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    deleted_user = User(id=row[0], name=row[1], email=row[2], subscribe=bool(row[3]))

    await conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    await conn.commit()
    await conn.close()

    return {"message": f'Пользователь {deleted_user.name} с id {deleted_user.id} удален'}
