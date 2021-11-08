from telegram.ext import Updater, dispatcher
from config import ENV
from config import CONFIG

if __name__ == '__main__':
    updater = Updater(token=ENV.BOT_TOKEN,use_context=True)
    dispatcher = updater.dispatcher

    me = updater.bot.get_me()
    CONFIG['ID'] = me.id
    CONFIG['Username'] = '@' + me.username
    print(f"Starting... ID: {str(CONFIG['ID'])} , Username: {CONFIG['Username']}")

    commands = []
    from cmdproc import worddict
    commands += worddict.add_dispatcher(dispatcher)

    updater.bot.set_my_commands(commands)

    updater.start_polling()
    print('Started...')

    updater.idle()
    print('Stopping...')
    print('Stopped.')