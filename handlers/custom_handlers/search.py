from telebot.types import Message
from states.states import States
from telebot.types import InputMediaPhoto

from utils.api import nasa_search

from loader import bot


@bot.message_handler(state=States.search)
def input_search_handler(message: Message) -> None:
    """
    Состояние ввода запроса пользователем

    :param message: введённый текст пользователя
    """
    text = message.text

    if text == "❌ Отменить операцию":
        bot.set_state(message.from_user.id, States.cancel, message.chat.id)
        bot.reply_to(message, "Вы сбросили состояние бота.")

    else:
        bot.set_state(message.from_user.id, "*", message.chat.id)

        search_list = nasa_search(message, text)
        """ Получение ссылок всех фото списком """

        if search_list:
            media_list = [InputMediaPhoto(photo) for photo in search_list]
            """ Преобразование всех ссылок фото в медиа группу """

            bot.send_media_group(message.chat.id, media_list, reply_to_message_id=message.id)

        else:
            bot.reply_to(message, f"По вашему запросу '{message.text}' ничего не найдено.")

        bot.send_message(message.chat.id, f"Если вы хотите выйти из поиска, нажмите кнопку "
                                          f"'❌ Отменить операцию'\n\nВведите следующий запрос:")
        bot.set_state(message.from_user.id, States.search, message.chat.id)
        """ Продолжение работы поиска """


@bot.message_handler(regexp="🔍 Поиск в NASA")
def search_handler(message: Message) -> None:
    """ Команда, запрашивающая информацию из библиотеки фото и видео NASA """
    bot.set_state(message.from_user.id, States.search, message.chat.id)

    text = "<b>🔍 Search</b>. Команда search предназначена для поиска информации в библиотеке " \
           "изображений и видео NASA. Первые записи начинаются в далёком 1920 году, но если вам " \
           "не нужны такие старые данные, то временной промежуток можно отрегулировать.\n\n" \
           "Для использования команды напишите информацию❗на <b><i>английском</i></b> языке❗ " \
           "который вы хотите найти:"

    bot.send_message(message.chat.id, text, parse_mode="html")
