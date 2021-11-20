from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext,MessageHandler, Filters
from json import load
from config import ENV
import random
from utils.filters import check_chatid_filter,check_admin_filter
from utils.fileproc import gen_irregular_dict_from_csv

word_dict = {}

def check_extra_dict(dict_dir):
    # 检查是否有用户自定义的单词库
    if dict_dir is None:
        return 0
    try:
        with open(f"{ENV.DATA_DIR}/res/iverbs.csv", 'r') as iverb_csvfile:
            with open(f'{ENV.DATA_DIR}/res/inouns.csv','r') as inouns_csvfile:
                word_dict = gen_irregular_dict_from_csv(
                    iverb_csvfile,
                    inouns_csvfile)
                print(f"Irregular单词条目：{len(word_dict)}个")
                return len(word_dict)
    except FileNotFoundError:
        return 0

def reload_dict():
    global word_dict
    with open('word_dict.json','r') as wd:
        word_dict = load(wd)
    
    try:
        with open(f"{ENV.DATA_DIR}/res/iverbs.csv", 'r') as iverb_csvfile:
            with open(f'{ENV.DATA_DIR}/res/inouns.csv','r') as inouns_csvfile:
                word_dict = gen_irregular_dict_from_csv(
                    iverb_csvfile,
                    inouns_csvfile,
                    word_dict)
    except FileNotFoundError:
        pass
reload_dict()

def get_answer(word):
    msg = ""
    if word in word_dict:
        for i in word_dict[word]:
            msg += i + "\n"
    return msg

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
    dp.add_handler(CommandHandler("t", wordtest_command))
    dp.add_handler(CommandHandler("timer", hour_game))
    return [BotCommand("t", "为特殊形态的单词们找伴儿游戏"),
            BotCommand("timer", "每小时推送个不规则形态单词给您")]