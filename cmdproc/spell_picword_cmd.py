import random
from pathlib import Path

from config import ENV
from dict.picture_dict import chapter_dict, word_dict
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.filters import check_chatid_filter

again = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎲 Play again 🕹", callback_data=f"getnewremember:"),
     InlineKeyboardButton("🧑🏻‍🏫 🗣Help 👩🏻‍🏫", callback_data=f"getpron:")
     ]])


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
        elif i == "-":
            show_word += "-"
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


def get_finish_view(msgs, words, data):
    # 要显示的已经达到了所有的word里最少的长度
    show_word = data[3]
    again_button = [[InlineKeyboardButton(
        "🎲 Play again 🕹", callback_data=f"getnewremember:")]]
    msg = msgs[0] + f"\nHints💡: {show_word}\n" + msgs[2] + "\n" + msgs[3]
    for w in words:
        again_button.append([InlineKeyboardButton(
            f"🧑🏻‍🏫 🗣Help {w} 👩🏻‍🏫", callback_data=f"getpron:{w}")])
    kb = InlineKeyboardMarkup(again_button)
    return msg, kb


def get_hint_view(msgs, show_count, keyboard):
    data = keyboard.inline_keyboard[0][0].callback_data.split(":")
    words = data[-2].split(" / ")
    show_word = get_show_words(words, show_count)
    msg = msgs[0] + f"\nHints💡: {show_word}\n" + msgs[2] + "\n" + msgs[3]
    keyboard.inline_keyboard[0][0].callback_data = f"rhit:{data[1]}:{data[2]}:{data[3]}:{show_count}"
    return msg, keyboard


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

    if show_count >= len(min(words, key=len)):
        msg, kb = get_finish_view(msgs, words, data)
        update.callback_query.edit_message_caption(
            msg + "\n😩 Are you kidding me! It’s sooooo easy! 😩", reply_markup=kb)
        query.answer("All the answers are for you!", show_alert=True)
    else:
        msg, keyboard = get_hint_view(msgs, show_count, keyboard)
        query.answer("💡💡💡💡")
        update.callback_query.edit_message_caption(msg, reply_markup=keyboard)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("m", remember_command))
    dp.add_handler(CallbackQueryHandler(
        remember_hit_callback, pattern="^rhit:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        remember_command, pattern="^getnewremember:"))
    return [BotCommand("m", "🎲 Play word Games 🕹")]
