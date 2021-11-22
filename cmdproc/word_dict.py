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
    msg += worddict.get_answer(word)
    # 单词发音
    msg += f"{pronouncing_dict.dict(word)}"
    # 单词词义
    msg += f"{msg}{wordnet_dict.dict(word)}"
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
    dp.add_handler(CommandHandler("p", pronounicing_command))
    dp.add_handler(CallbackQueryHandler(
        pronounicing_callback, pattern="^getpron:[A-Za-z0-9_]*"))
    return [BotCommand("p", "🧑🏻‍🏫 🗣Help 👩🏻‍🏫")]