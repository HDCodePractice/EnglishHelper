from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext
from telegram.ext import MessageHandler, Filters
from json import load
from config import ENV
import random

word_dict = {}
with open('pic_dict.json','r') as wd:
    word_dict = load(wd)

def check_answer(question,answer,filenumber):
    if answer.lower() in word_dict:
        words = word_dict[answer.lower()]
        for word in words:
            print(word,question,filenumber)
            if question == word["number"] and f"{filenumber}.jpg" == word["filename"]:
                return True
    return False

def remember_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    word = random.choice(list(word_dict.keys()))
    word = random.choice(word_dict[word])
    filenumber = word["filename"].split(".")[0]
    filename = f"res/picwords/{word['filename']}"
    number = word["number"]
    msg = f"图中的{number}\n是什么单词或短语\n请回复本消息回答你的答案。\nPage:{filenumber}"
    update.message.reply_photo(photo=open(filename,'rb'),caption=msg)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("m", remember_command))
    return [BotCommand("m", "看图想词游戏")]