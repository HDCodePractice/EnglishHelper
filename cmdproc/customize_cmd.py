import random
from json import load
from pathlib import Path

from config import ENV
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.fileproc import gen_pic_dict_from_csv
from utils.filters import check_chatid_filter
from cmdproc.picword import word_dict,chapter_dict


#reload_dict()
status = {"0":"✅","1":"❌","2":"⛔️"}
stored_data = dict()
#stored_data is to save previous status of configuration; for completed topic list, use chapter_dict
#data format should like this: {chapter1:[topic1,topic2,...,status],chapter2:[topic1,topic2,...,status],...}

def modify_chapter_status(chapter,topic,status):
    pass


def preview_chapter_dict():
    global stored_data
    if not stored_data: #如果stored_data是空的，就根据chapter_dict重新生成stored_data
        for key,val in chapter_dict.items():
            stored_data[key] = list(val.keys())
            stored_data[key] += status["0"]
    return stored_data

def reset_chapter_dict(): #初始化stored_data
    global stored_data
    stored_data.clear()


def update_finish_btn():
    pass

def update_chapter_list(user_id): #更新章节列表和按钮
    global stored_data
    menu_keyboard= []
    chapter_preview_msg = "Chapter List\n\n"
    finish_data = ""
    count = 1
    for key,value in stored_data.items():
        chapter_index  = list(stored_data.keys()).index(key) #计算store_data中的索引
        chapter_preview_msg += f"{count} {key} {value[-1]}\n"
        menu_keyboard.append([
            InlineKeyboardButton(text= f"{count} {value[-1]}", callback_data=f"custom-select:{key}:{value[-1]}:{user_id}"),
            InlineKeyboardButton(text=f"Choose {count} Topic", callback_data=f"custom-topic:{key}:{value[-1]}:{user_id}")
            ])
        if value[-1] == status["0"]:
            finish_data += f"{chapter_index}:"
        if value[-1] == status["2"]:
            selected_data = ""
            for selected_topic in value[:-1]:
                selected_data += f"-{value[:-1].index(selected_topic)}"
            finish_data += f"{chapter_index}{selected_data}:"
        count += 1

    
    menu_keyboard.append([
        InlineKeyboardButton(text=f"Finish",callback_data=f"custom-finish:{finish_data}{user_id}")
        ])
    return chapter_preview_msg,menu_keyboard

def update_topic_list(chapter_id,topic_id,chapter_status,user_id):
    global stored_data
    topic_list = list(chapter_dict[chapter_id].keys())
    chap_num = list(chapter_dict.keys()).index(chapter_id)
    selected_topic_list = stored_data[chapter_id]
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
        print(topic)
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
        #InlineKeyboardButton(text=f"Prev",callback_data=f"topic-prev:{prev_chap}:{user_id}"),
        InlineKeyboardButton(text=f"Back to Chapter List",callback_data=f"topic-back:{chap_num}:{topic_status_list}:{user_id}"),
        #InlineKeyboardButton(text=f"Next",callback_data=f"topic-next:{next_chap}:{user_id}")
        ])
    return topic_preview_msg,topic_menu_keyboard



#reset_chapter_dict()
preview_chapter_dict()

#@check_chatid_filter
def custom_chapter_command(update: Update, context: CallbackContext) -> None:
    incoming_message = update.effective_message
    user_id = incoming_message.from_user.id
    chapter_preview_msg,menu_keyboard = update_chapter_list(user_id)
    incoming_message.reply_markdown_v2(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

#@check_chatid_filter
def handle_menu_callback(update: Update, context: CallbackContext) -> None:
    global stored_data
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=2:
        return
    if data[0] == "custom-select":
        if data[-2] == status["0"]:
            new_stat = status["1"]
            for item in stored_data[data[1]][:-1]:
                stored_data[data[1]].remove(item)
        if data[-2] == status["1"] or data[-2] == status["2"]:
            new_stat = status["0"]
            for item in list(chapter_dict[data[1]].keys()):
                stored_data[data[1]].insert(0,item)
        stored_data[data[1]][-1] = new_stat
        chapter_preview_msg,menu_keyboard = update_chapter_list(data[-1])       
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

    if data[0] == "custom-topic":
        topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[2],data[-2],data[-1])  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "custom-finish":
        query.edit_message_text(text=f"设置结束！\n您所选择的设置为\n{str(stored_data)}\n\n请问需要开始游戏吗？")



def handle_topic_callback(update: Update, context: CallbackContext):
    global stored_data
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=2:
        return
    if data[0] == "topic-select":
        if data[-2] == status["0"]:
            new_stat = status["1"]
            stored_data[data[1]].remove(data[2])
        if data[-2] == status["1"]:
            new_stat = status["0"]
            stored_data[data[1]].insert(0,data[2])
        topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[2],new_stat,data[-1])  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "topic-back":
        target_topic = list(stored_data.keys())[int(data[1])]
        stored_data[target_topic] = []
        topic_list = data[-2].split(",")
        for topic_stat in topic_list[:-1]:
            if status["0"] in topic_stat.split("-")[1]:
                stored_data[target_topic].append(list(chapter_dict[target_topic].keys())[int(topic_stat.split("-")[0])])
        if len(stored_data[target_topic]) < len(topic_list[:-1]) and len(stored_data[target_topic]) > 0:
            new_stat = status["2"]
        elif len(stored_data[target_topic]) == len(topic_list[:-1]):
            new_stat = status["0"]
        else:
            new_stat = status["1"]
        stored_data[target_topic].append(new_stat)
        chapter_preview_msg,menu_keyboard = update_chapter_list(data[-1])    
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("c", custom_chapter_command))
 
    dp.add_handler(CallbackQueryHandler(
        handle_menu_callback, pattern="^custom-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        handle_topic_callback, pattern="^topic-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    return [BotCommand("c", "customize your game")]
