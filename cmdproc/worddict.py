from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext
from json import load
from config import ENV

word_dict = {}
with open('word_dict.json','r') as wd:
    word_dict = load(wd)

def worddict_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    query = context.args[0]
    if query in word_dict:
        msg = ""
        for i in word_dict[query]:
            msg += i + "\n"
        update.message.reply_text(msg)
    else:
        update.message.reply_text("您发的单词真的很普通，没啥特殊的。")
def add_dispatcher(dp):
    dp.add_handler(CommandHandler("i", worddict_command))
    return [BotCommand("i", "查询单词特殊形态")]