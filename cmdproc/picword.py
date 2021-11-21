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

again_button = [[InlineKeyboardButton(
    "🎲 Play again 🕹", callback_data=f"getnewremember:")]]


def check_answer(question, answer, filenumber):
    # 问题的答案是否正确
    # question : 图中的号码
    # answer : 用户回答的答案
    # filenumber : 图片的编号
    if answer.lower() in word_dict:
        words = word_dict[answer.lower()]
        for word in words:
            if question == word["number"] and f"{filenumber}.jpg" == word["filename"]:
                return True
    return False


def get_show_words(words, show_count):
    # 将一组词变化为*和原型
    # 如 [slacks,pants],show_count=3，则返回 "sl***s / pa**s"
    show_words = ""
    for w in words:
        show_words += f"{get_show_word(w,show_count)} / "
    return show_words[:-3]


def get_show_word(word, show_count):
    # 将一个单词的字母显示出来show_count个
    # 如 word = "hello" show_count = 3 则返回 "h**lo"
    show_word = ""
    for i in word:
        if i == " ":
            show_word += " "
        else:
            show_word += "*"
    for i in range(show_count):
        b = i + 1
        if b % 2 == 0:  # 偶数，后面加提示
            b = - b // 2
            if b == -1:
                show_word = show_word[:b] + word[b]
            else:
                show_word = show_word[:b] + word[b] + show_word[b+1:]
        else:
            b = b // 2
            show_word = show_word[:b] + word[b] + show_word[b+1:]
    return show_word


@check_chatid_filter
def remember_command(update: Update, context: CallbackContext) -> None:
    rword = random.choice(list(word_dict.keys()))
    word = random.choice(word_dict[rword])
    filenumber = word["filename"].split(".")[0]
    filename = f"{ENV.DATA_DIR}/res/picwords/{word['filename']}"
    if not Path(filename).is_file():
        filename = f"res/picwords/{word['filename']}"
        if not Path(filename).is_file():
            update.effective_message.reply_text(
                f"图片文件{word['filename']}不存在，请检你的字典")
    number = word["number"]
    chapter = word["chapter"]
    topic = word["topic"]
    dict_words = chapter_dict[chapter][topic][filenumber][number]
    show_word = ""
    data_word = ""
    for word in dict_words:
        show_word += f"{get_show_word(word,0)} / "
        data_word += f"{word} / "
    show_word = show_word[:-3]
    data_word = data_word[:-3]
    msg = f"☝️What's #{number}\nHints💡: {show_word}\nPage:{filenumber}\nReply this msg to submit the answer"
    buttons = [[
        InlineKeyboardButton("🙏 Click here for a 🔡 🙏", callback_data=f"rhit:{number}:{filenumber}:{data_word}:0")]]
    update.effective_message.reply_photo(
        photo=open(filename, 'rb'),
        caption=msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(buttons))


@check_chatid_filter
def remember_hit_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    if len(data) != 5:
        return
    keyboard = query.message.reply_markup
    msgs = query.message.caption.split("\n")
    words = data[3].split(" / ")
    show_count = int(data[4])+1
    show_word = ""

    if show_count >= len(min(words, key=len)):
        # 要显示的已经达到了所有的word里最少的长度
        show_word = data[3]
        msg = msgs[0] + f"\nHints💡: {show_word}\n" + msgs[2] + "\n" + msgs[3]
        for w in words:
            again_button.append([InlineKeyboardButton(
                f"🧑🏻‍🏫 🗣Help {w} 👩🏻‍🏫", callback_data=f"getpron:{w}")])
        kb = InlineKeyboardMarkup(again_button)

        update.callback_query.edit_message_caption(
            msg + "\n😩 Are you kidding me! It’s sooooo easy! 😩", reply_markup=kb)
        query.answer("All the answers are for you!", show_alert=True)
    else:
        show_word = get_show_words(words, show_count)
        msg = msgs[0] + f"\nHints💡: {show_word}\n" + msgs[2] + "\n" + msgs[3]
        keyboard.inline_keyboard[0][0].callback_data = f"rhit:{data[1]}:{data[2]}:{data[3]}:{show_count}"
        query.answer("💡💡💡💡")
        update.callback_query.edit_message_caption(msg, reply_markup=keyboard)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("m", remember_command))
    dp.add_handler(CallbackQueryHandler(
        remember_hit_callback, pattern="^rhit:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        remember_command, pattern="^getnewremember:"))
    return [BotCommand("m", "🎲 Play word Games 🕹")]
