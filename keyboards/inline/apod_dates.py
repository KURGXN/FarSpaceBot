from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def dates_markup() -> InlineKeyboardMarkup:
    """ Кнопки выбора даты APOD """
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="📅   Сегодня", callback_data="apod_today"),
               InlineKeyboardButton(text="📅   Другая дата", callback_data="apod_other_date"))

    return markup


def apod_menu() -> InlineKeyboardMarkup:
    """ Кнопка назад, возвращающая в меню APOD """
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="apod_menu"))

    return markup
