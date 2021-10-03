from glob import glob
from random import choice
import logging

from telegram.ext import CallbackContext
from telegram import Update

from utils import (get_smile, main_keyboard, play_random_numbers)


def start(update: Update, context: CallbackContext):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = f'Здравствуйте, {update.message.chat.username} ' \
           f'{context.user_data["emoji"]}'
    logging.info(text)
    update.message.reply_text(text, reply_markup=main_keyboard())


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
    update.message.reply_text(message, reply_markup=main_keyboard())


def talk_to_me(update: Update, context: CallbackContext):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_name = update.effective_user.first_name
    user_text = update.message.text
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}')
    update.message.reply_text(f'{user_name} {context.user_data["emoji"]}!')
    update.message.reply_text(f'Ты написал: {user_text}',
                              reply_markup=main_keyboard())


def send_cat_picture(update: Update, context: CallbackContext):
    cat_photos_list = glob('image/cat*.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb'),
        reply_markup=main_keyboard()
    )


def user_coordinates(update: Update, context: CallbackContext):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    logging.info(f'user: {update.effective_user.username} - coord: {coords}')
    update.message.reply_text(
        f'Ваши координаты {coords} {context.user_data["emoji"]}',
        reply_markup=main_keyboard())
