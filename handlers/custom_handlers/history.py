from telebot.types import Message
from database.users_database import get_history, clear_history

from loader import bot


@bot.message_handler(regexp="⏳ История запросов")
def history_handler(message: Message) -> None:
    """ Бот отображает все запросы пользователя """
    bot.reply_to(message, get_history(message), parse_mode="html")


@bot.message_handler(regexp="🧹 Очистить историю")
def clear_history_handler(message: Message) -> None:
    """ Бот очищает историю запросов пользователя в БД """
    bot.reply_to(message, clear_history(message))
