from pydantic import BaseModel


# Модель текстового сообщения
class MessageResponse(BaseModel):
    message: str


# Модель пользователя
class User(BaseModel):
    id: int
    name: str
    email: str
    subscribe: bool


# Модель пользователя для добавления нового в базу данных
class UserCreate(BaseModel):
    name: str
    email: str
    subscribe: bool


# Модель списка пользователей для возвращения всех пользователей
class UsersResponse(BaseModel):
    users: list[User]


# Модель отзыва
class Feedback(BaseModel):
    id: int
    user_id: int
    date: str
    text: str


# Модель отзыва, вместо поля user_id - имя пользователя
class FeedbackWithUser(BaseModel):
    id: int
    user: str
    date: str
    text: str


# Модель отзыва для добавления нового в базу данных
class FeedbackCreate(BaseModel):
    user_id: int
    text: str


# списка отзывов для возвращения всех отзывов
class FeedbackResponse(BaseModel):
    feedbacks: list[FeedbackWithUser]
