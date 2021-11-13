from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,CallbackContext,CallbackQueryHandler
from config import ENV
import pronouncing

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

def pronounicing_callback(update: Update, context: CallbackContext):
    pass

def pronounicing_command(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    word = context.args
    if len(word) == 0:
        update.effective_message.reply_text("请使用/p word来查询一个单词\n有关单词的发音规则参见 https://en.wikipedia.org/wiki/ARPABET ")
        return
    word = word[0]
    reslt = get_pronouncing(word)
    if len(reslt) == 0:
        update.effective_message.reply_text("在库存中没有找到这个单词的发音规则")
        return
    msg = ""
    count = 1
    for p in reslt:
        msg += f"{count}. [{p[0]}]\n"
        for r in p[1]:
            msg += f"{r} "
        msg = f"{msg[:-1]}\n\n"
        count += 1
    keyboard = [InlineKeyboardButton(f"google pronunciation:{word}", url=f"https://www.google.com/search?q={word}+pronunciation")]
    update.effective_message.reply_text(msg, reply_markup=InlineKeyboardMarkup([keyboard]))
    # TODO: 也许应该考虑使用多个按钮来分开，但是这样会比较麻烦
    # keyboard = []
    # for p in reslt:
    #     cbdata = ""
    #     for r in p[1]:
    #         cbdata += f"{r},"
    #     cbdata = f"pron:{p[0]}:{cbdata[:-1]}"
    #     keyboard.append([InlineKeyboardButton(p[0], callback_data=p[0])])
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text(f'Pronouncing of {word}', reply_markup=reply_markup)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("p", pronounicing_command))
    dp.add_handler(CallbackQueryHandler(pronounicing_callback,pattern="^pron:[A-Za-z0-9_]*"))
    return [BotCommand("p", "查询单词发音与类似发音的单词")]