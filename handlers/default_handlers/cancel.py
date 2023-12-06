from telebot.types import Message
from states.states import States

from loader import bot


@bot.message_handler(state=States.cancel)
@bot.message_handler(regexp="❌ Отменить операцию")
def cancel_state(message: Message) -> None:
    """ Отмена состояния командой, либо кнопкой назад """
    bot.reply_to(message, "Вы сбросили состояние бота.")
    bot.delete_state(message.from_user.id, message.chat.id)
