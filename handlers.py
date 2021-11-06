import logging
import os
from glob import glob
from random import choice

from telegram import Update
from telegram.ext import CallbackContext

from db import (db, get_or_create_user, change_avatar_db)
from utils import (main_keyboard, play_random_numbers)

subscribers = set()


def start(update: Update, context: CallbackContext):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    text = f'Здравствуйте, {update.message.chat.username} ' \
           f'{user["emoji"]}'
    logging.info(text)
    update.message.reply_text(text, reply_markup=main_keyboard())


def test(update: Update, context: CallbackContext):
    print(update.message.location)
    print(update.message.contact)
    print(dir(context))
    print(context)
    print(update)


def guess_number(update: Update, context: CallbackContext):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number, context)
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
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    user_text = update.message.text
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}')
    update.message.reply_text(f'{user["first_name"]} {user["emoji"]}!')
    update.message.reply_text(f'Ты написал: {user_text}',
                              reply_markup=main_keyboard())
    update.message.delete()


def send_cat_picture(update: Update, context: CallbackContext):
    cat_photos_list = glob('images/cat*.jpg')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb'),
        reply_markup=main_keyboard()
    )


def user_coordinates(update: Update, context: CallbackContext):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    coords = update.message.location
    logging.info(f'user: {update.effective_user.username} - coord: {coords}')
    update.message.reply_text(
        f'Ваши координаты {coords} {user["emoji"]}',
        reply_markup=main_keyboard())


def save_user_photo(update: Update, context: CallbackContext):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text('Файл сохранен')


def change_avatar(update: Update, context: CallbackContext):
    user = change_avatar_db(db, update.effective_user)
    update.message.reply_text(f'Готово: {user["emoji"]}')


def subscribe(update: Update, context: CallbackContext):
    subscribers.add(update.message.chat_id)
    update.message.reply_text('Вы подписались!')
    print(subscribers)


def unsubscribe(update: Update, context: CallbackContext):
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        update.message.reply_text('Вы отписались!')
    else:
        update.message.reply_text('Вы не подписаны, '
                                  'вы можете подписаться нажав на команду '
                                  '\n/subscribe')
    print(subscribers)


def callback_minute(context: CallbackContext):
    for chat_id in subscribers:
        context.bot.send_message(chat_id=chat_id,
                                 text='One message every minute')
        print('One message every minute')


def set_alarm(update: Update, context: CallbackContext):
    try:
        print(context.args)
        seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, seconds,
                                   context=update.message.chat_id)
    except (ValueError, IndexError):
        update.message.reply_text('Введите кол-во секунд после /alarm')


def alarm(context: CallbackContext):
    job = context.job
    context.bot.sendMessage(chat_id=job.context, text='Будильник сработал!')
