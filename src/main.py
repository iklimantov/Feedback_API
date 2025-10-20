from fastapi import FastAPI
from src.routers import users, feedbacks


app = FastAPI()


# Корневой эндпоинт проекта
@app.get('/')
def root():
    """Корневой метод проекта"""
    return {"message": "Это API, написанное на фреймворке FastAPI. Возможности: "
                       "Валидация запросов с помощью Pydantic, "
                       "Добавление новых пользователей, "
                       "Хранение и добавление новых отзывов."}

# Подключение роутеров
app.include_router(users.router)
app.include_router(feedbacks.router)
