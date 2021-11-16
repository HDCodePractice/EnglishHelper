from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext,MessageHandler, Filters
from config import ENV
import random
from cmdproc import picword
from cmdproc import worddict

def wordtest_reply(update: Update, context: CallbackContext) -> None:
    # 这个函数会处理所有的回复消息，独立出来，方便维护
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    if update.message.reply_to_message.caption:
        question = update.message.reply_to_message.caption.split("\n")[0]
    else:
        question = update.message.reply_to_message.text.split("\n")[0]
    answer = update.message.text.lower()
    if "☝️What's #" in question:   # 看图识字
        question = question.split("☝️What's #")[1]
        filenumber = update.message.reply_to_message.caption.split("\n")[-2].split("Page:")[1]
        if picword.check_answer(question, answer, filenumber):
            picword.again.inline_keyboard[0][1].callback_data = f"getpron:{answer}"
            update.message.reply_text(f"✌️ Bingo! {random.choice('👍🎉🎊')}",reply_markup=picword.again)
        else:
            update.message.reply_text("💔 Wrong answer！ Try again! {random.choice('🤣🤦🏻‍♀️🤦🏻🤦🏻‍♂️😭😱')}")
    else:  # 找同伴
        if question in worddict.word_dict:
            msg = ""
            correct = False
            for i in worddict.word_dict[question]:
                msg += i + "\n"
                if answer in i.split(" "):
                    correct = True
            if correct:
                update.message.reply_text(f"恭喜你，回答正确！\n{msg}")
            else:
                update.message.reply_text("回答错误，您可以再试一次。")

def add_dispatcher(dp):
    dp.add_handler(MessageHandler(Filters.text | Filters.reply, wordtest_reply))
    return []