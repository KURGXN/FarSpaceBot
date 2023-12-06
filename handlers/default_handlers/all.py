from telebot.types import Message
from keyboards.reply.menu import menu

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Хендлер ответа на пустые сообщения боту """
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Для использования бота выберите одну из кнопок снизу", reply_markup=menu())

