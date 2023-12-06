from keyboards.inline.apod_dates import dates_markup
from utils.api import get_apod_dict

from telebot.types import Message
from states.states import States

from loader import bot


@bot.message_handler(regexp="🔭 Астрономический снимок")
def apod_handler(message: Message) -> None:
    """
    Бот присылает астрономический снимок по выбранной дате,
    его название и описание
    """
    text = "<b>🔭  Астрономический снимок дня</b> - один из самых популярных сайтов NASA. " \
           "Его популярность можно сравнить с видео Джастина Бибера. " \
           "Каждый день вы можете получать новые астрономические снимки или видео, сделанные " \
           "космическими телескопами где-то далеко от Земли\n\n" \
           "<i>Для использования команды выберите дату для Астрономического снимка:</i>"
    bot.send_message(message.chat.id, text, reply_markup=dates_markup(), parse_mode="html")


@bot.message_handler(state=States.apod_date)
def apod_date_handler(message: Message) -> None:
    """
    Состояние ввода даты для снимка apod

    :param message: введённый текст пользователя
    """
    date = message.text

    if date == "❌ Отменить операцию":
        bot.set_state(message.from_user.id, States.cancel, message.chat.id)
        bot.reply_to(message, "Вы сбросили состояние бота.")
        """ Если пользователь нажимает на кнопку отмены, то бот ставит состояние cancel """
    else:
        bot.send_message(message.chat.id, get_apod_dict(message, date), reply_markup=dates_markup())
