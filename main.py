import logging

from telegram.ext import (Updater, Filters,
                          CommandHandler, MessageHandler, ConversationHandler)

import settings
from handlers import (start, guess_number, talk_to_me, send_cat_picture,
                      user_coordinates, save_user_photo, test, change_avatar,
                      form_start, form_name, form_rating, form_skip,
                      form_comment, form_dontknow)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def create_dp(bot):
    dp = bot.dispatcher

    form = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заполнить форму)$'),
                                     form_start)],
        states={
            'name': [MessageHandler(Filters.text, form_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'),
                                      form_rating)],
            'comment': [
                CommandHandler('skip', form_skip),
                MessageHandler(Filters.text, form_comment)
            ]
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document
            | Filters.location, form_dontknow)]
    )

    dp.add_handler(form)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'),
                                  send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватар)$'),
                                  change_avatar))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.contact, test))
    dp.add_handler(MessageHandler(Filters.photo, save_user_photo))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


if __name__=='__main__':
    mybot = Updater(settings.API_KEY)

    logging.info('Бот запущен')

    create_dp(mybot)

    mybot.start_polling()
    mybot.idle()
