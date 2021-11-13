from telegram import Update, BotCommand
from telegram.ext import CommandHandler,CallbackContext,MessageHandler, Filters
from json import load
from config import ENV
import random
from cmdproc import picword


word_dict = {}
with open('word_dict.json','r') as wd:
    word_dict = load(wd)

def worddict_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    if  len(context.args) == 0:
        update.message.reply_text("你没有提交单词，正确的打开方式为： /i word")
        return
    query = context.args[0]
    if query in word_dict:
        msg = ""
        for i in word_dict[query]:
            msg += i + "\n"
        update.message.reply_text(msg)
    else:
        update.message.reply_text("您发的单词真的很普通，没啥特殊的。")

def wordtest_command(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    word = random.choice(list(word_dict.keys()))
    update.message.reply_text(f"{word}\n的同伴有谁？\n请回复本消息回答你的答案。")

def wordtest_reply(update: Update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    if update.message.reply_to_message.caption:
        question = update.message.reply_to_message.caption.split("\n")[0]
    else:
        question = update.message.reply_to_message.text.split("\n")[0]
    answer = update.message.text.lower()
    if "图中的" in question:   # 看图识字
        question = question.split("图中的")[1]
        filenumber = update.message.reply_to_message.caption.split("\n")[-1].split("Page:")[1]
        if picword.check_answer(question, answer, filenumber):
            picword.again.inline_keyboard[0][1].callback_data = f"getpron:{answer}"
            update.message.reply_text("回答正确！",reply_markup=picword.again)
        else:
            update.message.reply_text("回答错误，挖空脑髓再想想？")
    else:                     # 找同伴
        if question in word_dict:
            msg = ""
            correct = False
            for i in word_dict[question]:
                msg += i + "\n"
                if answer in i.split(" "):
                    correct = True
            if correct:
                update.message.reply_text(f"恭喜你，回答正确！\n{msg}")
            else:
                update.message.reply_text("回答错误，您可以再试一次。")

def send_reply_msg(context : CallbackContext):
    word = random.choice(list(word_dict.keys()))
    context.bot.send_message(chat_id=-1001409640737, 
                    text=f'{word}\n的同伴有谁？\n请回复本消息回答你的答案。')

def hour_game(update, context: CallbackContext) -> None:
    if str(update.effective_chat.id) not in ENV.CHATIDS:
        return
    context.job_queue.run_repeating(send_reply_msg, interval=3600, first=1)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("i", worddict_command))
    dp.add_handler(CommandHandler("t", wordtest_command))
    dp.add_handler(CommandHandler("timer", hour_game))
    dp.add_handler(MessageHandler(Filters.text | Filters.reply, wordtest_reply))
    return [BotCommand("i", "查询单词特殊形态"),
            BotCommand("t", "为特殊形态的单词们找伴儿游戏"),
            BotCommand("timer", "每小时推送个不规则形态单词给您")]