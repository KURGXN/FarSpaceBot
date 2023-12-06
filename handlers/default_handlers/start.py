from telebot.types import Message
from telebot.apihelper import ApiTelegramException

from keyboards.reply.menu import menu

from loader import bot


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    """ Хендлер команды /start. Бот приветствует пользователя """
    try:
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEKsphlSK8hRMnUJMBrLjayQbjwifWYGAACagADwZxgDCHf0XJEvU3QMwQ")
    except ApiTelegramException as i_exc:
        print(f"{i_exc}\nСтикер не найден, возможно неправильно написан id стикера.")

    bot.reply_to(message, f"Рад вас видеть, <b>{message.from_user.first_name} "
                          f"{message.from_user.last_name}</b>!\n\n", parse_mode="html")
    bot.send_message(message.chat.id, "Для использования бота выберите одну из кнопок снизу", reply_markup=menu())
