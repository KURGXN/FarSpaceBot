from loader import bot
import handlers  # noqa
from telebot.custom_filters import StateFilter

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    print('Бот запущен.')
    bot.infinity_polling()
    print('Бот завершил работу.')
