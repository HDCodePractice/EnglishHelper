from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext
from telegram.ext import MessageHandler, Filters
from json import load
from config import ENV
import random

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

def wordtest_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    word = random.choice(list(word_dict.keys()))
    update.message.reply_text(f"{word}\n的同伴有谁？\n请回复本消息回答。")

def wordtest_reply(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    question = update.message.reply_to_message.text.split("\n")[0]
    answer = update.message.text
    if question in word_dict:
        msg = ""
        correct = False
        for i in word_dict[question]:
            msg += i + "\n"
            if answer in i.split(" "):
                correct = True
        if correct:
            update.message.reply_text(f"恭喜你，回答正确！\n{msg}")
        else:
            update.message.reply_text("回答错误，您可以再试一次。")

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("i", worddict_command))
    dp.add_handler(CommandHandler("t", wordtest_command))
    dp.add_handler(MessageHandler(Filters.text | Filters.reply, wordtest_reply))
    return [BotCommand("i", "查询单词特殊形态"),
            BotCommand("t", "为特殊形态的单词们找伴儿")]