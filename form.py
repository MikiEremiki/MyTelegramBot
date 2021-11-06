from telegram import (ReplyKeyboardMarkup, Update, ReplyKeyboardRemove,
                      ParseMode)
from telegram.ext import CallbackContext, ConversationHandler

from utils import main_keyboard


id_messages = set()


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


def del_messages(update: Update, context: CallbackContext):
    for id_message in id_messages:
        context.bot.delete_message(update.message.chat_id, id_message)
    id_messages.clear()
