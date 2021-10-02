from settings import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(update: Update, context: CallbackContext):
    text = 'вызвана команда /start'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(update: Update, context: CallbackContext):
    user_text = update.message.text
    logging.info(f'User: {update.message.chat.username}, '
                 f'chatid: {update.message.chat.id}, '
                 f'text: {update.message.text}')
    update.message.reply_text(user_text)


def main():
    mybot = Updater(API_KEY)

    logging.info('Бот запущен')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()