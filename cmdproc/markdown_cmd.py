from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler


def test_markdown(update: Update, context: CallbackContext) -> None:
    index = update.effective_message.text.find(" ")
    msg = update.effective_message.text[index+1:]
    try:
        update.effective_message.reply_text(msg, parse_mode="MarkdownV2")
    except BadRequest as e:
        update.effective_message.reply_text(e.message)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("testmd", test_markdown))
    return []
