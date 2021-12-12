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
status = {"0":"✅","1":"❌","2":"⛔️"}
stored_data = dict()
#stored_data is to save previous status of configuration; for completed topic list, use chapter_dict
#data format should like this: {uid: {chapter1:[topic1,topic2],[topic3,topic4]},{chapter2:[topic1,topic2],[]},...}



def preview_chapter_dict(uid):
    user_data = fetch_user_data(uid)
    if user_data == None: #如果stored_data是空的，就根据chapter_dict重新生成stored_data
        user_data ={}
        for key,val in chapter_dict.items():
            user_data[key] = []
            user_data[key].append(list(val.keys()))
            user_data[key].append(list())
    return user_data


def fetch_user_data(uid):
    user_chapter_dict = read_file_to_dict("user_chapter_dict.json")
    if user_chapter_dict:
        if uid in list(user_chapter_dict.keys()) and user_chapter_dict[uid]: 
            return user_chapter_dict[uid]
    return None

def update_data_to_file(data,filename):
    try:
        user_chapter_dict = read_file_to_dict("user_chapter_dict.json")
        for key,value in data.items():
            user_chapter_dict[key] = value
        user_chapter_dict = json.dumps(user_chapter_dict)
        with open(filename,"w") as f:
                f.write(f"{user_chapter_dict}")
        return True
    except Exception as e:
        return False

#unused function,but keep it for future use
# def convert_data_to_json(uid,data):
#     '''
#     data format: 0-0-1:1:2:3:4:5:6:7:8: 
#     initial stored_data: {'Computer': [['Program'], []], 
#                    'Health': [['The Body', 'Symptoms and Injuries'], []], 
#                    'Community': [['Downtown'], []], 
#                    'Everyday Language': [['Time', 'The Calendar'], []], 
#                    'People': [['Feelings'], []], 
#                    '': [['The Home'], []], 
#                    'Housing': [['A House and Yard'], []], 
#                    'Food': [['Back from the Market', 'Fruit', 'Vegetables', 'A Coffee Shop Menu'], []], 
#                    'Clothing': [['Everyday Clothes', 'Casual,Work,and Formal Clothes', 'Seasonal Clothing'], []]}
    
#     '''
#     stored_data = preview_chapter_dict(uid)
#     chapter_list = list(stored_data.keys())
#     user_chapter_list = data.split(':')[1:-1]
#     for chapter in user_chapter_list:
#         topic_list = list(chapter_dict[chapter_list[int(chapter)]].keys())
#         print(topic_list)
#         user_topic_list = chapter.split('-')
#         if len(topic_list) > 1:
#             stored_data[chapter_list[int(chapter)]] = []
#             seleted_topic_list = []
#             unseleted_topic_list = []
#             for topic in user_topic_list:
#                 if user_topic_list.index(topic) in topic_list[1:]:
#                     seleted_topic_list.append(topic)
#                 else:
#                     unseleted_topic_list.append(topic)
#         stored_data[chapter_list[int(chapter)]].append(seleted_topic_list)
#         stored_data[chapter_list[int(chapter)]].append(unseleted_topic_list)
#     return stored_data

# def update_finish_btn():
#     pass

def update_chapter_list(user_id,stored_data): #更新章节列表和按钮
    menu_keyboard= []
    chapter_preview_msg = "Chapter List\n\n"
    count = 1
    for key,value in stored_data.items():
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
    selected_topic_list = stored_data[chapter_id][0]
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
    global stored_data
    incoming_message = update.effective_message
    user_id = incoming_message.from_user.id
    stored_data = preview_chapter_dict(str(user_id))
    chapter_preview_msg,menu_keyboard = update_chapter_list(user_id,stored_data)
    incoming_message.reply_markdown_v2(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

@check_chatid_filter
def handle_menu_callback(update: Update, context: CallbackContext) -> None:
    global stored_data
    incoming_callback_query = update.callback_query
    user_id = incoming_callback_query.from_user.id
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=1:
        return
    if data[0] == "custom-select":
        if data[-2] == status["0"]:
            stored_data[data[1]] = []
            stored_data[data[1]].append(list())
            stored_data[data[1]].append(list(chapter_dict[data[1]].keys()))           
        if data[-2] == status["1"] or data[-2] == status["2"]:
            stored_data[data[1]]=[]
            stored_data[data[1]].append(list(chapter_dict[data[1]].keys()))
            stored_data[data[1]].append(list()) 
        chapter_preview_msg,menu_keyboard = update_chapter_list(data[-1],stored_data)       
        query.edit_message_text(text=chapter_preview_msg,reply_markup=InlineKeyboardMarkup(menu_keyboard))

    if data[0] == "custom-topic":
        topic_preview_msg,topic_menu_keyboard = update_topic_list(data[1],data[-1],stored_data)  
        query.edit_message_text(text=topic_preview_msg,reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "custom-finish":
        user_id = data[-1]
        saved_data = {}
        saved_data[user_id] = stored_data
        update_data_to_file(saved_data,"user_chapter_dict.json")
        display_data={}
        for key,value in stored_data.items():
            if value[0]:
                display_data[key]=value[0]
        query.edit_message_text(text=f"设置已保存!\n您所选择的设置为\n{str(display_data)}\n\n请使用/m开始游戏!\n\n您也可以使用/c再次更改您的设置")



@check_chatid_filter
def handle_topic_callback(update: Update, context: CallbackContext):
    global stored_data
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <=2:
        return
    if data[0] == "topic-select":
        if data[-2] == status["0"]:
            stored_data[data[1]][0].remove(data[2])
            stored_data[data[1]][1].append(data[2])
        if data[-2] == status["1"]:
            stored_data[data[1]][1].remove(data[2])
            stored_data[data[1]][0].append(data[2])
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
