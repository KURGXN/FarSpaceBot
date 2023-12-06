from config_data.config import API_KEY, RAPID_KEY
from database.users_database import add_user
from telebot.types import Message, CallbackQuery
from typing import Dict

import requests
import json
import re


def get_apod_dict(message: (Message, CallbackQuery), date: str) -> Dict or str:
    """
    Функция, получающая астрономический снимок от NASA API

    :param message: сообщение пользователя
    :param date: дата снимка для добавления в БД
    :returns: словарь APOD
    """
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
             message.from_user.last_name, f"Запрос apod. Дата: {date}")
    """ Добавление запроса пользователя в базу данных User """

    i_url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}"
    i_req = requests.get(i_url, timeout=10)  # timeout=10, если не будет ответа от сервера то бот выдаст ошибку

    i_dict = json.loads(i_req.text)
    """ Сразу преобразование ответа в словарь, т.к. если даже api выдаст ошибку, то это будет словарь """

    if i_req.status_code != 200:
        return f"Ошибка {i_dict['code']}. {translate_text(i_dict['msg'])}\n\n" \
               f"Если вы хотите выйти из снимка, нажмите кнопку '❌ Отменить операцию'\n\n" \
               f"Выберите другую дату:"
    """ Если что-то пошло не так при запросе, то NASA API выдаёт ответ словарем со """
    """ статусом ошибки и соответствующим сообщением """

    return f"{i_dict['date']}\n\n" \
           f"{translate_text(i_dict['title'])}\n\n{translate_text(i_dict['explanation'])}\n\n" \
           f"{i_dict['url']}\n\n"


def translate_text(text: str) -> str:
    """
    Функция, переводящая текст через rapid api

    :param text: сообщение на английском для перевода
    :return: переведённый текст на русском языке
    """
    url = "https://translate-plus.p.rapidapi.com/translate"

    payload = {
        "text": text,
        "source": "en",
        "target": "ru"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "translate-plus.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code != 200:
        raise ConnectionAbortedError("Нет ответа от сервера.")

    return response.json()["translations"]["translation"]


def nasa_search(message: (Message, CallbackQuery), text: str, media_type="image") -> Dict or str:
    """ Получение фото/видео из библиотеки NASA по запросу пользователя """
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
             message.from_user.last_name, f"Запрос search. Текст: {text}")
    """ Добавление запроса пользователя в базу данных User """

    i_url = f"https://images-api.nasa.gov/search?q={text}&media_type={media_type}"
    i_req = requests.get(i_url, timeout=10)  # timeout=10, если не будет ответа от сервера то бот выдаст ошибку

    i_dict = json.loads(i_req.text)
    """ Сразу преобразование ответа в словарь, т.к. если даже api выдаст ошибку, то это будет словарь """

    if i_req.status_code != 200:
        return i_dict
    """ Если что-то пошло не так при запросе, то NASA API выдаёт ответ словарем со """
    """ статусом ошибки и соответствующим сообщением """

    images = re.findall(r"https://images-assets\S+.jpg", i_req.text)
    """ Поиск всех изображений в словаре """

    return images[:10]
