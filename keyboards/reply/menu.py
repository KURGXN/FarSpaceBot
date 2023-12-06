from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def menu() -> ReplyKeyboardMarkup:
    """ Главное меню """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔭 Астрономический снимок"), KeyboardButton("🔍 Поиск в NASA"))
    markup.add(KeyboardButton("⏳ История запросов"), KeyboardButton("🧹 Очистить историю"))
    markup.add((KeyboardButton("❌ Отменить операцию")))

    return markup
