from telegram.ext import Updater, dispatcher

from config import CONFIG, ENV

if __name__ == '__main__':
    updater = Updater(token=ENV.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    me = updater.bot.get_me()
    CONFIG['ID'] = me.id
    CONFIG['Username'] = '@' + me.username
    print(
        f"Starting... ID: {str(CONFIG['ID'])} , Username: {CONFIG['Username']}")

    commands = []
    from cmdproc import word_in_pic_cmd
    commands += word_in_pic_cmd.add_dispatcher(dispatcher)
    from cmdproc import spell_picword_cmd
    commands += spell_picword_cmd.add_dispatcher(dispatcher)
    from cmdproc import word_dict
    commands += word_dict.add_dispatcher(dispatcher)
    from cmdproc import worddict
    commands += worddict.add_dispatcher(dispatcher)
    from cmdproc import upload
    commands += upload.add_dispatcher(dispatcher)
    from cmdproc import grammar_cmd
    commands += grammar_cmd.add_dispatcher(dispatcher)
    from cmdproc import markdown_cmd
    commands += markdown_cmd.add_dispatcher(dispatcher)
    from cmdproc import start_cmd
    commands += start_cmd.add_dispatcher(dispatcher)

    # 这个import必须放在最后，因为它的MessageHandler会吃掉所有的消息
    from cmdproc import replyanswer
    commands += replyanswer.add_dispatcher(dispatcher)

    updater.bot.set_my_commands(commands)

    updater.start_polling()
    print('Started...')

    updater.idle()
    print('Stopping...')
    print('Stopped.')
