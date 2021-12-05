import random

from config import ENV
from telegram import BotCommand, Update
from telegram.ext import CallbackContext, Filters, MessageHandler
from utils.filters import check_chatid_filter

from cmdproc import picword, worddict, wordpic


@check_chatid_filter
def wordtest_reply(update: Update, context: CallbackContext) -> None:
    # 这个函数会处理所有的回复消息，独立出来，方便维护
    if update.message.reply_to_message.caption:
        question = update.message.reply_to_message.caption.split("\n")[0]
    else:
        question = update.message.reply_to_message.text.split("\n")[0]
    answer = update.message.text.lower()
    if "☝️What's #" in question:   # 看图识字
        question_data = update.message.reply_to_message.reply_markup.inline_keyboard[
            0][0].callback_data
        if "rhit:" in question_data:
            # rhit:{number}:{filenumber}:{data_word}:0
            questions = question_data.split(":")[3].split("/")
            questions = [q.lower() for q in questions]
            if answer in questions:
                picword.again.inline_keyboard[0][1].callback_data = f"getpron:{answer}"
                update.message.reply_text(
                    f"✌️ Bingo! {random.choice('👍🎉🎊')}", reply_markup=picword.again)
            else:
                update.message.reply_text(
                    f"💔 Wrong answer！ Try again! {random.choice('💔🤣🤦🏻😭😱')}")
        else:
            return
    elif "☝️What's" in question and "#" not in question:  # 看字识图
        question = question.split("☝️What's ")[1]
        question_data = update.message.reply_to_message.reply_markup.inline_keyboard[
            0][0].callback_data
        if "ahit:" in question_data:
            # ahit:{number}:{filenumber}:{word[0]
            data1 = question_data.split(":")[1]
            if answer == data1.lower():
                wordpic.again.inline_keyboard[0][1].callback_data = f"getpron:{question}"
                update.message.reply_text(
                    f"✌️ Bingo! {random.choice('👍🎉🎊')}", reply_markup=wordpic.again)
            else:
                update.message.reply_text(
                    f"💔 Wrong answer！ Try again! {random.choice('💔🤣🤦🏻😭😱')}")
    else:  # 找同伴
        if question in worddict.word_dict:
            msg = ""
            correct = False
            for i in worddict.word_dict[question]:
                msg += i + "\n"
                if answer in i.split(" "):
                    correct = True
            if correct:
                update.message.reply_text(
                    f"✌️ Bingo! {random.choice('👍🎉🎊')}！\n{msg}")
            else:
                update.message.reply_text(
                    f"💔 Wrong answer！Try again! {random.choice('💔🤣🤦🏻😭😱')}")


def add_dispatcher(dp):
    dp.add_handler(MessageHandler(
        Filters.text | Filters.reply, wordtest_reply))
    return []
