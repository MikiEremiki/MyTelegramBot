import logging
from random import randint, choice
from glob import glob

from telegram.ext import Updater, CallbackContext, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import Update
from emoji import emojize

import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def get_smile():
    smile = choice(settings.USER_EMOJI)
    smile = emojize(smile, use_aliases=True)
    return smile


def start(update: Update, context: CallbackContext):
    smile = get_smile()
    text = f'Здравствуйте, {update.message.chat.username} {smile}'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(update: Update, context: CallbackContext):
    smile = get_smile()
    user_name = update.effective_user.first_name
    user_text = update.message.text
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}')
    update.message.reply_text(f'{user_name} {smile}!')
    update.message.reply_text(f'Ты написал: {user_text}')


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ' \
                  f'ты выиграл!'
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, " \
                  f"я выиграл!"
    return message


def guess_number(update: Update, context: CallbackContext):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите целое число'
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}, '
                 f'text_from: {message}'
                 )
    update.message.reply_text(message)


def send_cat_picture(update: Update, context: CallbackContext):
    cat_photos_list = glob('image/cat*.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb')
    )


def create_dp(bot):
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


if __name__ == '__main__':
    mybot = Updater(settings.API_KEY)

    logging.info('Бот запущен')

    create_dp(mybot)

    mybot.start_polling()
    mybot.idle()
