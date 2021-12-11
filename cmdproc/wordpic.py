import random
from json import load
from pathlib import Path

from config import ENV
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from cmdproc import picword

again = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎲 Play again 🕹", callback_data=f"getnew:mm"),
     InlineKeyboardButton("🧑🏻‍🏫 🗣Help 👩🏻‍🏫", callback_data=f"getpron:")
     ]])


# def check_answer(question, answer, filenumber):
#     # 问题的答案是否正确
#     # question : 图中的单词
#     # answer : 用户回答的号码
#     # filenumber : 图片的页数编号
#     for x in question.lower().split("/"):
#         if x in picword.word_dict:
#             words = picword.word_dict[x]
#             for word in words:
#                 if answer == word["number"] and f"{filenumber}.jpg" == word["filename"]:
#                     return True
#     return False


def map_word_to_pic_command(update: Update, context: CallbackContext) -> None:
    word = random.choice(list(picword.word_dict.keys()))
    slices = picword.word_dict[word]
    for slice in slices:
        filename = f"{ENV.DATA_DIR}/res/picwords/{slice['filename']}"
        if not Path(filename).is_file():
            filename = f"res/picwords/{slice[0]['filename']}"
            if not Path(filename).is_file():
                update.effective_message.reply_text(
                    f"图片文件{slice['filename']}不存在，请检你的字典")
    slice = random.choice(picword.word_dict[word])
    filenumber = slice["filename"].split(".")[0]
    filename = f"{ENV.DATA_DIR}/res/picwords/{slice['filename']}"
    msg = f"☝️Where is {word}\nPage: {filenumber}\nReply this msg using the matched number"
    number = slice["number"]
    buttons = [[
        InlineKeyboardButton("🙏 Click here for an answer 🙏", callback_data=f"ahit:{number}:{filenumber}:{word}")]]
    update.effective_message.reply_photo(
        photo=open(filename, 'rb'),
        caption=msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(buttons))


def map_word_to_pic_hit_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    if len(data) != 4:
        return
    keyboard = query.message.reply_markup
    msgs = query.message.caption.split("\n")
    again_button = [[InlineKeyboardButton(
        "🎲 Play again 🕹", callback_data=f"getnew:mm")]]
    msg = f"☝️{data[3]} is at {data[1]}" + "\n" + msgs[1] + "\n" + msgs[2]
    for word in data[3].split("/"):
        again_button.append([InlineKeyboardButton(
            f"🧑🏻‍🏫 🗣Help {word} 👩🏻‍🏫", callback_data=f"getpron:{word}")])
    kb = InlineKeyboardMarkup(again_button)
    update.callback_query.edit_message_caption(
        msg + "\n😩 Are you kidding me! It’s sooooo easy! 😩", reply_markup=kb)
    query.answer("All the answers are for you!", show_alert=True)


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("mm", map_word_to_pic_command))
    dp.add_handler(CallbackQueryHandler(
        map_word_to_pic_hit_callback, pattern="^ahit:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        map_word_to_pic_command, pattern="^getnew:mm"))
    return [BotCommand("mm", "🎲 Play word-pic Games 🕹")]
