from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,CallbackContext,CallbackQueryHandler
from config import ENV
import pronouncing
import random
from utils.filters import check_chatid_filter

def get_rhyme(p):
    """
    Returns the rhyme of the pronouncing.
    """
    return [w for w in pronouncing.rhyme_lookup.get(pronouncing.rhyming_part(p), [])
                if w != p]

def get_pronouncing(word):
    """
    Returns the pronunciation of the word.
    """
    reslt = []
    ps = pronouncing.phones_for_word(word)
    for p in ps:
        reslt.append([p, get_rhyme(p)])
    return reslt

def get_answer(word):
    keyboard = [
        [InlineKeyboardButton(
            f"google pronunciation", 
            url=f"https://www.google.com/search?q={word}+pronunciation")],
        [InlineKeyboardButton(
            f"google translate",
            url=f"https://translate.google.com/#view=home&op=translate&sl=en&tl=zh-CN&text={word}")],
        [InlineKeyboardButton(
            f"youglish",
            url=f"https://youglish.com/pronounce/{word}/english/us?")],
        [InlineKeyboardButton(
            f"youtube pronunciation",
            url=f"https://www.youtube.com/results?search_query={word}+pronunciation")],
    ]
    reslt = get_pronouncing(word)
    if len(reslt) == 0:
        return ["Go to the vast Internet and look it up~",keyboard]
    msg = ""
    count = 1
    for p in reslt:
        msg += f"{count}. [{p[0]}]\n"
        near = [w for w in p[1] if w != word]
        if len(near) > 20:
            near = random.sample(near, 20)
        for r in near:
            msg += f"{r} "
        msg = f"{msg[:-1]}\n\n"
        count += 1
    return [f"{word:}\n{msg}",keyboard]

@check_chatid_filter
def pronounicing_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    word = query.data.split(":")[1]
    msg,keyboard = get_answer(word)
    update.effective_message.reply_text(
        msg, 
        quote=False, 
        reply_markup=InlineKeyboardMarkup(keyboard)
        )

@check_chatid_filter
def pronounicing_command(update: Update, context: CallbackContext):
    word = context.args
    if len(word) == 0:
        update.effective_message.reply_text("请使用/p word来查询一个单词\n有关单词的发音规则参见 https://en.wikipedia.org/wiki/ARPABET ")
        return
    word = word[0]
    msg,keyboard = get_answer(word)
    update.effective_message.reply_text(
        msg,
        quote=False,
        reply_markup=InlineKeyboardMarkup(keyboard)
        )

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("p", pronounicing_command))
    dp.add_handler(CallbackQueryHandler(pronounicing_callback,pattern="^getpron:[A-Za-z0-9_]*"))
    return [BotCommand("p", "🧑🏻‍🏫 🗣Help 👩🏻‍🏫")]