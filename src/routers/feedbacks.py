from fastapi import APIRouter, HTTPException
from src.db.database import get_connection
from src.models.schemas import FeedbackResponse, Feedback, FeedbackCreate
from datetime import datetime


router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


# Получение списка всех отзывов из базы данных
@router.get("/", response_model=FeedbackResponse)
def get_feedbacks():
    """
    Получение списка всех отзывов
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT f.id, u.name, f.date, f.text
    FROM feedbacks f
    JOIN users u ON f.user_id = u.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    feedbacks = [
        {
            "id": row[0],
            "user": row[1],
            "date": row[2],
            "text": row[3]
        }
        for row in rows
    ]
    return {"feedbacks": feedbacks}


# Добавление нового отзыва в базу данных
@router.post('/', response_model=Feedback)
def add_feedback(feedback: FeedbackCreate):
    """
    Добавляет новый отзыв в базу данных.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Проверим, существует ли пользователь с таким user_id
    cursor.execute("SELECT id FROM users WHERE id = ?", (feedback.user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Вставка нового отзыва
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    cursor.execute(
        "INSERT INTO feedbacks (user_id, date, text) VALUES (?, ?, ?)",
        (feedback.user_id, now, feedback.text)
    )
    conn.commit()
    feedback_id = cursor.lastrowid
    conn.close()

    return Feedback(id=feedback_id, user_id=feedback.user_id,
                    date=now,
                    text=feedback.text)
