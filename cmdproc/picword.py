from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler,CallbackContext,CallbackQueryHandler
from json import load
from config import ENV
import random
from utils.filters import check_chatid_filter

word_dict = {}
with open('pic_dict.json','r') as wd:
    word_dict = load(wd)
chapter_dict = {}
with open('chapter_dict.json','r') as wd:
    chapter_dict = load(wd)

again = InlineKeyboardMarkup([
    [InlineKeyboardButton("🎲 Play again 🕹",callback_data=f"getnewremember:"),
    InlineKeyboardButton("🧑🏻‍🏫 🗣Help 👩🏻‍🏫",callback_data=f"getpron:")
    ]])

def check_answer(question,answer,filenumber):
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

def get_show_word(word,show_count):
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
        if b % 2 == 0: # 偶数，后面加提示
            b =  - b // 2
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
    rword = "slacks" #random.choice(list(word_dict.keys()))
    word = random.choice(word_dict[rword])
    filenumber = word["filename"].split(".")[0]
    filename = f"res/picwords/{word['filename']}"
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
        InlineKeyboardButton("🙏 Click here for a 🔡 🙏",callback_data=f"rhit:{number}:{filenumber}:{data_word}:0")]]
    update.effective_message.reply_photo(
        photo=open(filename,'rb'),
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
    word = data[3]
    words = word.split("/")
    show_word = ""
    for word in words:
        word = word.strip()
        show_count = int(data[4])+1
        if show_count < len(word):
            show_count = show_count
        else:    
            show_count = len(word)
        print(show_count)
        show_word += f"{get_show_word(word,show_count)} / "
    show_word = show_word[:-3]
    msg = msgs[0] + f"\nHints💡: {show_word}\n" + msgs[2] + "\n" + msgs[3]
    keyboard.inline_keyboard[0][0].callback_data = f"rhit:{data[1]}:{data[2]}:{data[3]}:{show_count}"
    print(keyboard)
    print(len(max(words, key=len))-1)
    if show_count < len(max(words, key=len))-1 and "*" in show_word:
        update.callback_query.edit_message_caption(msg,reply_markup=keyboard)
        query.answer("💡💡💡💡")
    if "*" not in show_word:
        again.inline_keyboard[0][1].callback_data = f"getpron:{word}"
        update.callback_query.edit_message_caption(msg + "\n😩 Are you kidding me! It’s sooooo easy! 😩",reply_markup=again)
        query.answer("All the answers are for you!",show_alert=True)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("m", remember_command))
    dp.add_handler(CallbackQueryHandler(remember_hit_callback,pattern="^rhit:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(remember_command,pattern="^getnewremember:"))
    return [BotCommand("m", "🎲 Play word Games 🕹")]