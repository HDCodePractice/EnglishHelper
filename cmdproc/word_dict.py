from functools import reduce

from config import ENV
from dict import pronouncing_dict, wordnet_dict
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.filters import check_chatid_filter

from cmdproc import worddict


def get_answer(word):
    keyboard = [
        [InlineKeyboardButton(
            f"google pronunciation",
            url=f"https://www.google.com/search?q={word}+pronunciation")],
        [InlineKeyboardButton(
            f"google translate",
            url=f"https://translate.google.com/#view=home&op=translate&sl=en&text={word}")],
        [InlineKeyboardButton(
            f"youglish",
            url=f"https://youglish.com/pronounce/{word}/english/us?")],
        [InlineKeyboardButton(
            f"urban dictionary",
            url=f"https://www.urbandictionary.com/define.php?term={word}")],
        [InlineKeyboardButton(
            f"youtube pronunciation",
            url=f"https://www.youtube.com/results?search_query={word}+pronunciation")],
    ]

    # 单词提示产
    msg = f"{word}:\n"
    # 单词特殊形式说明
    irg = worddict.get_answer(word)
    if len(irg) > 0:
        msg += f"{irg}\n\n"
    # 单词发音
    p = pronouncing_dict.dict(word)
    if len(p) > 0:
        msg += f"{p}\n\n"
    s = wordnet_dict.get_synonyms_antonyms_msg(word)
    if len(s) > 0:
        msg += f"{s}\n\n"
    # 单词词义
    msg += f"{wordnet_dict.dict(word)}"

    if msg == f"{word}:\n":
        msg = f"{word}:\nGo to Internet ~"
    return [msg, keyboard]


@check_chatid_filter
def pronounicing_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    word = query.data.split(":")[1]
    msg, keyboard = get_answer(word)
    update.effective_message.reply_text(
        msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@check_chatid_filter
def pronounicing_command(update: Update, context: CallbackContext):
    word = context.args
    if len(word) == 0:
        update.effective_message.reply_text(
            "请使用/p word来查询一个单词\n有关单词的发音规则参见 https://en.wikipedia.org/wiki/ARPABET ")
        return
    word = reduce(lambda x, y: x+" "+y, word)
    msg, keyboard = get_answer(word)
    update.effective_message.reply_text(
        msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def add_dispatcher(dp):
    wordnet_dict.download_wordnet()
    dp.add_handler(CommandHandler("p", pronounicing_command))
    dp.add_handler(CallbackQueryHandler(
        pronounicing_callback, pattern="^getpron:[A-Za-z0-9_]*"))
    return [BotCommand("p", "🧑🏻‍🏫 🗣Help 👩🏻‍🏫")]
