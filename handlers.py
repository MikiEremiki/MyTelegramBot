from glob import glob
import os
from random import choice
import logging

from telegram.ext import CallbackContext, ConversationHandler
from telegram import (Update, ReplyKeyboardRemove, ReplyKeyboardMarkup,
                      ParseMode)

from main import subscribers
from utils import (get_smile, main_keyboard, play_random_numbers)


def start(update: Update, context: CallbackContext):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = f'Здравствуйте, {update.message.chat.username} ' \
           f'{context.user_data["emoji"]}'
    logging.info(text)
    update.message.reply_text(text, reply_markup=main_keyboard())


def test(update: Update, context: CallbackContext):
    print(update.message.location)
    print(update.message.contact)
    # print(dir(context))
    print(context.user_data)
    # print(update.message)


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
    context.user_data['emoji'] = get_smile(context.user_data)
    emo = context.user_data['emoji']
    user_name = update.effective_user.first_name
    user_text = update.message.text
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}')
    update.message.reply_text(f'{user_name} {emo}!')
    update.message.reply_text(f'Ты написал: {user_text}',
                              reply_markup=main_keyboard())


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
    context.user_data['emoji'] = get_smile(context.user_data)
    emo = context.user_data['emoji']
    coords = update.message.location
    logging.info(f'user: {update.effective_user.username} - coord: {coords}')
    update.message.reply_text(
        f'Ваши координаты {coords} {emo}',
        reply_markup=main_keyboard())


def save_user_photo(update: Update, context: CallbackContext):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text('Файл сохранен')


def change_avatar(update: Update, context: CallbackContext):
    if 'emoji' in context.user_data:
        del context.user_data['emoji']
    context.user_data['emoji'] = get_smile(context.user_data)
    emo = context.user_data['emoji']
    update.message.reply_text(f'Готово: {emo}')


def form_start(update: Update, context: CallbackContext):
    update.message.reply_text('Как вас зовут? Напишите ваши имя и фамилию.',
                              reply_markup=ReplyKeyboardRemove())
    return 'name'


def form_name(update: Update, context: CallbackContext):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Пожалуйста, напишите имя и фамилию')
        return 'name'
    else:
        context.user_data['form'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Оцените бота шкале от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True,
                                             resize_keyboard=True)
        )
        return 'rating'


def form_rating(update: Update, context: CallbackContext):
    context.user_data['form']['rating'] = int(update.message.text)

    update.message.reply_text(
        'Оставьте комментарий в свободной форме или пропустите этот шаг, '
        'введя /skip'
    )
    return 'comment'


def form_skip(update: Update, context: CallbackContext):
    user_text = f"""
<b>Имя Фамилия:</b> {context.user_data['form']['name']}
<b>Оценка:</b> {context.user_data['form']['rating']}"""

    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def form_comment(update: Update, context: CallbackContext):
    context.user_data['form']['comment'] = update.message.text
    user_text = f"""
<b>Имя Фамилия:</b> {context.user_data['form']['name']}
<b>Оценка:</b> {context.user_data['form']['rating']}
<b>Комментарий:</b> {context.user_data['form']['comment']}"""

    update.message.reply_text(user_text, reply_markup=main_keyboard(),
                              parse_mode=ParseMode.HTML)
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
