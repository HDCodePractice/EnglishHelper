import random
from json import load
from pathlib import Path

from config import ENV
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.fileproc import gen_pic_dict_from_csv
from utils.filters import check_chatid_filter

word_dict = {}
chapter_dict = {}


def check_extra_dict(dict_dir):
    # 检查是否有用户自定义的单词库
    if dict_dir is None:
        return 0
    try:
        with open(f"{dict_dir}/res/picwords.csv", 'r') as csvfile:
            word_dict, chapter_dict = gen_pic_dict_from_csv(csvfile)
            print(f"看图识词单词条目：{len(word_dict)}个")
            return len(word_dict)
    except FileNotFoundError:
        return 0


def reload_dict():
    global word_dict
    global chapter_dict
    # 加载内置单词库
    with open('pic_dict.json', 'r') as wd:
        word_dict = load(wd)
    with open('chapter_dict.json', 'r') as wd:
        chapter_dict = load(wd)

    # 加载用户自定义单词库
    try:
        with open(f"{ENV.DATA_DIR}/res/picwords.csv", 'r') as csvfile:
            word_dict, chapter_dict = gen_pic_dict_from_csv(
                csvfile, word_dict, chapter_dict)
    except FileNotFoundError:
        pass


reload_dict()

again = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎲 Play again 🕹", callback_data=f"getnew:mm"),
     InlineKeyboardButton("🧑🏻‍🏫 🗣Help 👩🏻‍🏫", callback_data=f"getpron:")
     ]])


def check_answer(question, answer, filenumber):
    # 问题的答案是否正确
    # question : 图中的单词
    # answer : 用户回答的号码
    # filenumber : 图片的页数编号
    if question.lower() in word_dict:
        words = word_dict[question.lower()]
        for word in words:
            if answer == word["number"] and f"{filenumber}.jpg" == word["filename"]:
                return True
    return False


def mm_command(update: Update, context: CallbackContext) -> None:
    chapter = random.choice(list(chapter_dict.keys()))
    topic = random.choice(list(chapter_dict[chapter].keys()))
    filenumber = random.choice(list(chapter_dict[chapter][topic].keys()))
    number = random.choice(
        list(chapter_dict[chapter][topic][filenumber].keys()))
    word = chapter_dict[chapter][topic][filenumber][number]
    slice = word_dict[word[0]][0]
    filename = f"{ENV.DATA_DIR}/res/picwords/{slice['filename']}"
    if not Path(filename).is_file():
        filename = f"res/picwords/{slice['filename']}"
        if not Path(filename).is_file():
            update.effective_message.reply_text(
                f"图片文件{slice['filename']}不存在，请检你的字典")
    msg = f"☝️What's {word[0]}\nPage:{filenumber}\nReply this msg using the matched number"
    buttons = [[
        InlineKeyboardButton("🙏 Click here for an answer 🙏", callback_data=f"ahit:{number}:{filenumber}:{word[0]}")]]
    update.effective_message.reply_photo(
        photo=open(filename, 'rb'),
        caption=msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(buttons))


def mm_hit_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    if len(data) != 4:
        return
    keyboard = query.message.reply_markup
    msgs = query.message.caption.split("\n")
    again_button = [[InlineKeyboardButton(
        "🎲 Play again 🕹", callback_data=f"getnew:mm")]]
    msg = f"☝️{data[3]} is at {data[1]}" + msgs[1] + "\n" + msgs[2]
    again_button.append([InlineKeyboardButton(
        f"🧑🏻‍🏫 🗣Help {data[3]} 👩🏻‍🏫", callback_data=f"getpron:{data[3]}")])
    kb = InlineKeyboardMarkup(again_button)
    update.callback_query.edit_message_caption(
        msg + "\n😩 Are you kidding me! It’s sooooo easy! 😩", reply_markup=kb)
    query.answer("All the answers are for you!", show_alert=True)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("mm", mm_command))
    dp.add_handler(CallbackQueryHandler(
        mm_hit_callback, pattern="^ahit:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        mm_command, pattern="^getnew:mm"))
    return [BotCommand("mm", "🎲 Play word-pic Games 🕹")]
