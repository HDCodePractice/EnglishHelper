import json
from pathlib import Path

from config import ENV
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.fileproc import gen_pic_dict_from_csv,read_file_to_dict
from utils.filters import check_chatid_filter
from cmdproc.picword import chapter_dict
#reload_dict()
#stored_data is to save previous status of configuration; for completed topic list, use chapter_dict
#data format should like this: {chapter1:[topic1,topic2,...,status],chapter2:[topic1,topic2,...,status],...}

def gen_chapter_list(user_id,stored_data): #更新章节列表和按钮
    menu_keyboard= []
    chapter_preview_msg = "Chapter List\n\n"
    count = 1
    for key,value in stored_data.items():
        chapter_preview_msg += f"{count} {key}\n"
        menu_keyboard.append([ 
            InlineKeyboardButton(text=f"Choose {count} Topic", callback_data=f"preview-chapter-topic:{key}:{user_id}")
            ])
        count += 1
    
    menu_keyboard.append([
        InlineKeyboardButton(text=f"Finish",callback_data=f"preview-chapter-finish:{user_id}")
        ])
    return chapter_preview_msg,menu_keyboard

def gen_topic_list(chapter_id,user_id,stored_data):
    topic_list = list(chapter_dict[chapter_id].keys()) #获取数据库中的所有topic列表
    chap_num = list(chapter_dict.keys()).index(chapter_id) #获取用户选取的topic
    if chap_num == 0:
        prev_chap = "None"
    if chap_num == len(list(chapter_dict.keys())) - 1:
        next_chap = "None"
    if chap_num > 0:
        prev_chap = list(chapter_dict.keys())[chap_num - 1]
    if chap_num < len(list(chapter_dict.keys())):
        next_chap = list(chapter_dict.keys())[chap_num + 1]
    topic_preview_msg = f"Topic List\nChapter Name:{chapter_id}\n\n"
    topic_menu_keyboard = []
    count = 1
    for topic in topic_list:
        topic_preview_msg += f"{count} {topic}\n"
        count += 1
    topic_menu_keyboard.append([
        InlineKeyboardButton(text=f"Prev",callback_data=f"preview-topic-page:{prev_chap}:{user_id}"),
        InlineKeyboardButton(text=f"Back to Chapter List",callback_data=f"preview-topic-back:{chap_num}:{user_id}"),
        InlineKeyboardButton(text=f"Next",callback_data=f"preview-topic-page:{next_chap}:{user_id}")
        ])
    return topic_preview_msg,topic_menu_keyboard



@check_chatid_filter
def preview_chapter_command(update: Update, context: CallbackContext) -> None:
    incoming_message = update.effective_message
    user_id = incoming_message.from_user.id
    chapter_preview_msg,menu_keyboard = gen_chapter_list(user_id,chapter_dict)
    incoming_message.reply_markdown_v2(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

@check_chatid_filter
def handle_preview_chapter_callback(update: Update, context: CallbackContext) -> None:
    incoming_callback_query = update.callback_query
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=1:
        return
    if data[0] == "preview-chapter-topic":
        topic_preview_msg,topic_menu_keyboard = gen_topic_list(data[1],data[-1],chapter_dict)  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "preview-chapter-finish":
        query.edit_message_text(text=f"预览结束!您可以使用/m开始游戏!\n或者使用/c设置您想要玩的章节和题目\n")




def handle_preview_topic_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=1:
        return
    if data[0] == "preview-topic-page":
        if data[1] != "None":
            topic_preview_msg,topic_menu_keyboard = gen_topic_list(data[1],data[-1],chapter_dict)
            query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))
    if data[0] == "preview-topic-back":
        chapter_preview_msg,menu_keyboard = gen_chapter_list(data[-1],chapter_dict)    
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("v", preview_chapter_command))
 
    dp.add_handler(CallbackQueryHandler(
        handle_preview_chapter_callback, pattern="^preview-chapter-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        handle_preview_topic_callback, pattern="^preview-topic-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    return [BotCommand("v", "view chapter and topic list")]
