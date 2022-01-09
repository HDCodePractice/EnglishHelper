import json
from pathlib import Path

from config import ENV
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.fileproc import gen_pic_dict_from_csv,read_file_to_dict
from utils.filters import check_chatid_filter,check_callback_user
from dict.picture_dict import chapter_dict
from dict.user_chapter_dict import stored_data,set_user_config,clear_user_config,update_data_to_file,gen_user_chapter_dict

#reload_dict()
status = {"0":"✅","1":"❌","2":"⛔️"}


def update_chapter_list(user_id,stored_data): #更新章节列表和按钮
    menu_keyboard= []
    chapter_preview_msg = "Chapter List\n\n"
    count = 1
    for key,value in stored_data[user_id].items():
        if not value[0]:
            over_status = status["1"]
        elif not value[1]:
            over_status = status["0"]
        else:
            over_status = status["2"]
        chapter_preview_msg += f"{count} {key} {over_status}\n"
        menu_keyboard.append([
            InlineKeyboardButton(text= f"{count} {over_status}", callback_data=f"custom-select:{key}:{over_status}:{user_id}"),
            InlineKeyboardButton(text=f"Choose {count} Topic", callback_data=f"custom-topic:{key}:{over_status}:{user_id}")
            ])
        count += 1
    
    menu_keyboard.append([
        InlineKeyboardButton(text=f"Finish",callback_data=f"custom-finish:{user_id}")
        ])
    return chapter_preview_msg,menu_keyboard

def update_topic_list(chapter_id,user_id,stored_data):
    topic_list = list(chapter_dict[chapter_id].keys()) #获取数据库中的所有topic列表
    chap_num = list(chapter_dict.keys()).index(chapter_id) #获取用户选取的topic
    selected_topic_list = stored_data[user_id][chapter_id][0]
    topic_status_list = ""
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
        topic_index = topic_list.index(topic)
        if topic in selected_topic_list:
            topic_status = status["0"]
        else:
            topic_status = status["1"]
        topic_preview_msg += f"{count} {topic} {topic_status}\n"
        topic_status_list += f"{topic_index}-{topic_status},"
        topic_menu_keyboard.append([
            InlineKeyboardButton(text=f"{count} {topic_status}",callback_data=f"topic-select:{chapter_id}:{topic}:{topic_status}:{user_id}")
            ])
        count += 1
    topic_menu_keyboard.append([
        InlineKeyboardButton(text=f"Prev",callback_data=f"topic-page:{prev_chap}:{user_id}"),
        InlineKeyboardButton(text=f"Back to Chapter List",callback_data=f"topic-back:{chap_num}:{topic_status_list}:{user_id}"),
        InlineKeyboardButton(text=f"Next",callback_data=f"topic-page:{next_chap}:{user_id}")
        ])
    return topic_preview_msg,topic_menu_keyboard



@check_chatid_filter
def custom_chapter_command(update: Update, context: CallbackContext) -> None:
    incoming_message = update.effective_message
    user_id = incoming_message.from_user.id
    gen_user_chapter_dict(str(user_id))
    chapter_preview_msg,menu_keyboard = update_chapter_list(str(user_id),stored_data)
    incoming_message.reply_markdown_v2(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

@check_chatid_filter
def handle_menu_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    reply_user_id = update.effective_user.id
    reply_user_name = update.effective_user.full_name
    #如果不是提问人的id， 回复信息
    alert_msg = f"亲爱的{reply_user_name}, 这个不是你的游戏设置，请不要随意点击!\n如果想要设置单词游戏，请自己输入命令/c\n"
    if check_callback_user(str(reply_user_id),data[-1]) == False:
        update.callback_query.answer(alert_msg,show_alert=True)
        return
    if len(data) <=1:
        return
    if data[0] == "custom-select":
        if data[-2] == status["0"]:
            set_user_config(data[-1],data[1],[list(),list(chapter_dict[data[1]].keys())])         
        if data[-2] == status["1"] or data[-2] == status["2"]:
            set_user_config(data[-1],data[1],[list(chapter_dict[data[1]].keys()),list()])
        chapter_preview_msg,menu_keyboard = update_chapter_list(data[-1],stored_data)       
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

    if data[0] == "custom-topic":
        topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[-1],stored_data)  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "custom-finish":
        filename = f"{ENV.DATA_DIR}/user_chapter_dict.json"
        update_data_to_file(data[-1],filename)
        display_data={}
        for key,value in stored_data[data[-1]].items():
            if value[0]:
                display_data[key]=value[0]
        query.edit_message_text(text=f"设置已保存!\n您所选择的设置为\n{str(display_data)}\n\n请使用/m开始游戏!\n\n您也可以使用/c再次更改您的设置")



@check_chatid_filter
def handle_topic_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(":")
    reply_user_id = update.effective_user.id
    reply_user_name = update.effective_user.full_name
    #如果不是提问人的id， 回复信息
    alert_msg = f"亲爱的{reply_user_name}, 这个不是你的游戏设置，请不要随意点击!\n如果想要设置单词游戏，请自己输入命令/c\n"
    if check_callback_user(str(reply_user_id),data[-1]) == False:
        update.callback_query.answer(alert_msg,show_alert=True)
        return
    if len(data) <=2:
        return
    if data[0] == "topic-select":
        if data[-2] == status["0"]:
            set_user_config(data[-1],data[1],[list(),list(chapter_dict[data[1]].keys())])
        if data[-2] == status["1"]:
            set_user_config(data[-1],data[1],[list(chapter_dict[data[1]].keys()),list()])
        topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[-1],stored_data)  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))
    if data[0] == "topic-page":
        if data[1] != "None":
            topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[-1],stored_data)
            query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))
    if data[0] == "topic-back":
        chapter_preview_msg,menu_keyboard = update_chapter_list(data[-1],stored_data)    
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("c", custom_chapter_command))
 
    dp.add_handler(CallbackQueryHandler(
        handle_menu_callback, pattern="^custom-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        handle_topic_callback, pattern="^topic-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    return [BotCommand("c", "configure chapter and topic you want to play")]
