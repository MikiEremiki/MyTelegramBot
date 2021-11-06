from glob import glob
import os
from random import choice
import logging

from telegram.ext import CallbackContext, ConversationHandler
from telegram import (Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,
                      ParseMode)

from bot import subscribers
from utils import (main_keyboard, play_random_numbers)
from db import (db, get_or_create_user, change_avatar_db)


id_messages = set()


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


def form_start(update: Update, context: CallbackContext):
    reply = update.message.reply_text(
        'Как вас зовут? Напишите ваши имя и фамилию.',
        reply_markup=ReplyKeyboardRemove())
    id_messages.add(reply.message_id)
    return 'name'


def form_name(update: Update, context: CallbackContext):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        reply = update.message.reply_text('Пожалуйста, напишите имя и фамилию')
        id_messages.add(update.message.message_id)
        id_messages.add(reply.message_id)
        return 'name'
    else:
        context.user_data['form'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        reply = update.message.reply_text(
            'Оцените бота шкале от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True,
                                             resize_keyboard=True)
        )
        id_messages.add(update.message.message_id)
        id_messages.add(reply.message_id)
        return 'rating'


def form_rating(update: Update, context: CallbackContext):
    context.user_data['form']['rating'] = int(update.message.text)

    reply = update.message.reply_text(
        'Оставьте комментарий в свободной форме или пропустите этот шаг, '
        'введя /skip'
    )
    id_messages.add(update.message.message_id)
    id_messages.add(reply.message_id)
    return 'comment'


def form_skip(update: Update, context: CallbackContext):
    user_text = f"""
<b>Имя Фамилия:</b> {context.user_data['form']['name']}
<b>Оценка:</b> {context.user_data['form']['rating']}"""

    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    id_messages.add(update.message.message_id)
    del_messages(update, context)
    return ConversationHandler.END


def form_comment(update: Update, context: CallbackContext):
    context.user_data['form']['comment'] = update.message.text
    user_text = f"""
<b>Имя Фамилия:</b> {context.user_data['form']['name']}
<b>Оценка:</b> {context.user_data['form']['rating']}
<b>Комментарий:</b> {context.user_data['form']['comment']}"""

    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    id_messages.add(update.message.message_id)
    del_messages(update, context)
    return ConversationHandler.END


def form_dontknow(update: Update, context: CallbackContext):
    update.message.reply_text('Не понимаю')


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


def del_messages(update: Update, context: CallbackContext):
    for id_message in id_messages:
        context.bot.delete_message(update.message.chat_id, id_message)
    id_messages.clear()
