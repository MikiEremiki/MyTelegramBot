import logging

from telegram.ext import (Updater, Filters,
                          CommandHandler, MessageHandler, ConversationHandler)

import settings
import handlers
import form

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def create_dp(bot: Updater):
    dp = bot.dispatcher

    form_hd = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заполнить форму)$'),
                                     form.form_start)],
        states={
            'name': [MessageHandler(Filters.text, form.form_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'),
                                      form.form_rating)],
            'comment': [
                CommandHandler('skip', form.form_skip),
                MessageHandler(Filters.text, form.form_comment)
            ]
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document
            | Filters.location, form.form_dontknow)]
    )

    dp.add_handler(form_hd)
    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CommandHandler('test', handlers.test))
    dp.add_handler(CommandHandler('guess', handlers.guess_number))
    dp.add_handler(CommandHandler('cat', handlers.send_cat_picture))
    dp.add_handler(CommandHandler('subscribe', handlers.subscribe))
    dp.add_handler(CommandHandler('unsubscribe', handlers.unsubscribe))
    dp.add_handler(CommandHandler('alarm', handlers.set_alarm))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'),
                                  handlers.send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватар)$'),
                                  handlers.change_avatar))
    dp.add_handler(MessageHandler(Filters.location, handlers.user_coordinates))
    dp.add_handler(MessageHandler(Filters.contact, handlers.test))
    dp.add_handler(MessageHandler(Filters.photo, handlers.save_user_photo))
    dp.add_handler(MessageHandler(Filters.text, handlers.talk_to_me))


if __name__ == '__main__':
    mybot = Updater(settings.API_KEY, use_context=True)

    logging.info('Бот запущен')

    create_dp(mybot)

    mybot.job_queue.run_repeating(handlers.callback_minute, interval=10)

    mybot.start_polling()
    mybot.idle()
