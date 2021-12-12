from dict import grammar_dict, picture_dict
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def help_cmd(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(f"""
I have a big English knowledge base.
Picture words:{len(picture_dict.word_dict)}
English grammar:{len(grammar_dict.grammar_dict)}
    """
                                        )


def start_cmd(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "Welecome.You can visit our wiki https://github.com/HDCodePractice/EnglishHelper/wiki get help.", quote=False)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("start", start_cmd))
    return []
