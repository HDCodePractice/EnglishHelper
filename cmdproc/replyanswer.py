from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters
from config import ENV
import random
from cmdproc import picword
from cmdproc import worddict
from utils.filters import check_chatid_filter


@check_chatid_filter
def wordtest_reply(update: Update, context: CallbackContext) -> None:
    # 这个函数会处理所有的回复消息，独立出来，方便维护
    if update.message.reply_to_message.caption:
        question = update.message.reply_to_message.caption.split("\n")[0]
    else:
        question = update.message.reply_to_message.text.split("\n")[0]
    answer = update.message.text.lower()
    if "☝️What's #" in question:   # 看图识字
        question = question.split("☝️What's #")[1]
        filenumber = update.message.reply_to_message.caption.split(
            "\n")[-2].split("Page:")[1]
        if picword.check_answer(question, answer, filenumber):
            picword.again.inline_keyboard[0][1].callback_data = f"getpron:{answer}"
            update.message.reply_text(
                f"✌️ Bingo! {random.choice('👍🎉🎊')}", reply_markup=picword.again)
        else:
            update.message.reply_text(
                f"💔 Wrong answer！ Try again! {random.choice('🤣🤦🏻‍♀️🤦🏻🤦🏻‍♂️😭😱')}")
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
                    f"💔 Wrong answer！Try again! {random.choice('💔🤣🤦🏻‍♀️🤦🏻🤦🏻‍♂️😭😱')}")


def add_dispatcher(dp):
    dp.add_handler(MessageHandler(
        Filters.text | Filters.reply, wordtest_reply))
    return []
