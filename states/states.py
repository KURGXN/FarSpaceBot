from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    """ Состояния бота """
    apod_date = State()
    search = State()
    cancel = State()
