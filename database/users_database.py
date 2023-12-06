import os
from peewee import *
from telebot.types import Message


db = SqliteDatabase(os.path.join("database", "users_db.db"))
""" Инициализация базы данных """


class User(Model):
    """ Модель, описывающая пользователя в телеграм чате """
    user_id = IntegerField()
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)
    user_request = CharField()

    class Meta:
        database = db


def add_user(user_id: int, username: str, first_name: str, last_name: str, user_request: str) -> None:
    """ Добавление запроса пользователя в БД User """
    User.create(user_id=user_id, username=username, first_name=first_name,
                last_name=last_name, user_request=user_request)


def get_history(message: Message) -> str:
    """ Получение истории запросов пользователя """
    user_list = [user.user_request for user in User.select() if user.user_id == message.from_user.id]
    text = "\n▫ ".join(user_list)

    if len(text) == 0:
        return f"Ваша история запросов пустая, <b>{message.from_user.first_name}:</b>"
    """ Если история запросов пустая, то бот отправит соответствующее сообщение"""

    return f"Ваша история запросов, <b>{message.from_user.first_name}:</b>\n\n" \
           f"▫ {text}\n\n"


def clear_history(message: Message) -> str:
    """ Очистка истории запросов пользователя """
    query = User.delete().where(User.user_id == message.from_user.id)
    query.execute()

    return "Ваша история запросов очищена"
