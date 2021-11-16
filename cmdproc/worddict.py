from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext,MessageHandler, Filters
from json import load
from config import ENV
import random
from utils.filters import check_chatid_filter,check_admin_filter


word_dict = {}
with open('word_dict.json','r') as wd:
    word_dict = load(wd)

@check_chatid_filter
def worddict_command(update: Update, context: CallbackContext) -> None:
    if  len(context.args) == 0:
        update.message.reply_text("你没有提交单词，正确的打开方式为： /i word")
        return
    query = context.args[0]
    if query in word_dict:
        msg = ""
        for i in word_dict[query]:
            msg += i + "\n"
        update.message.reply_text(msg)
    else:
        update.message.reply_text("您发的单词真的很普通，没啥特殊的。")

@check_chatid_filter
def wordtest_command(update: Update, context: CallbackContext) -> None:
    word = random.choice(list(word_dict.keys()))
    update.message.reply_text(f"{word}\n的同伴有谁？\n请回复本消息回答你的答案。")

def send_reply_msg(context : CallbackContext):
    word = random.choice(list(word_dict.keys()))
    context.bot.send_message(chat_id=-1001409640737, 
                    text=f'{word}\n的同伴有谁？\n请回复本消息回答你的答案。')

@check_admin_filter
@check_chatid_filter
def hour_game(update, context: CallbackContext) -> None:
    context.job_queue.run_repeating(send_reply_msg, interval=3600, first=1)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("i", worddict_command))
    dp.add_handler(CommandHandler("t", wordtest_command))
    dp.add_handler(CommandHandler("timer", hour_game))
    return [BotCommand("i", "查询单词特殊形态"),
            BotCommand("t", "为特殊形态的单词们找伴儿游戏"),
            BotCommand("timer", "每小时推送个不规则形态单词给您")]