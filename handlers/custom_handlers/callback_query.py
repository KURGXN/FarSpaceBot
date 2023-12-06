from keyboards.inline.apod_dates import apod_menu, dates_markup
from utils.api import get_apod_dict
from telebot.types import CallbackQuery
from states.states import States

from datetime import datetime

from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery) -> None:
    """ Обработчик запросов """
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "apod_today":  # Сегодняшняя дата для APOD
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=get_apod_dict(call, datetime.now().date()))
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=dates_markup())

    elif call.data == "apod_other_date":  # Дата пользователя для APOD
        bot.set_state(call.from_user.id, States.apod_date, call.message.chat.id)
        """ Состояние ввода даты для пользователя """

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["bot_message"] = call.message
        """ Сохранение сообщения от бота, чтобы удалить его после ответа пользователя """

        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text="Введите дату астрономического снимка от 1995-06-16"
                                   " в формате год-месяц-день:", parse_mode="html")
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=apod_menu())

    elif call.data == "apod_menu":  # Меню APOD
        bot.set_state(call.from_user.id, "*", call.message.chat.id)
        """ Сброс состояния бота """

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату для Астрономического снимка:")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=dates_markup())
