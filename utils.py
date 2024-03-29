from random import randint

from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    my_contact = KeyboardButton('Мой контакт', request_contact=True)
    my_location = KeyboardButton('Мои координаты', request_location=True)
    return ReplyKeyboardMarkup([
        [my_contact, my_location],
        ['Прислать котика', 'Сменить аватар', 'Заполнить форму']
    ], resize_keyboard=True)


def play_random_numbers(user_number, context):
    emo = context.user_data['emoji']
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты {emo} загадал {user_number}, я загадал {bot_number}, ' \
                  f'ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты {emo} загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты {emo} загадал {user_number}, я загадал {bot_number}, ' \
                  f'я выиграл!'
    return message
