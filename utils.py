from random import randint, choice

from telegram import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

import settings


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def main_keyboard():
    my_contact = KeyboardButton('Мой контакт', request_contact=True)
    my_location = KeyboardButton('Мои координаты', request_location=True)
    return ReplyKeyboardMarkup([
        [my_contact, my_location],
        ['Прислать котика', 'Заполнить анкету']
    ], resize_keyboard=True)


def play_random_numbers(user_number, context):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты {context.user_data["emoji"]} загадал {user_number}, я загадал {bot_number}, ' \
                  f'ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты {context.user_data["emoji"]} загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты {context.user_data["emoji"]} загадал {user_number}, я загадал {bot_number}, ' \
                  f'я выиграл!'
    return message
