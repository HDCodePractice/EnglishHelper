import json
from pathlib import Path

from config import ENV
from dict.picture_dict import chapter_dict
from dict.user_chapter_dict import ( gen_user_chapter_dict,
                                    set_user_config, get_user_topic_config,get_chapter_list,get_user_chapter_config,
                                    display_user_config,update_data_to_file)
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from utils.filters import check_callback_user, check_chatid_filter

# reload_dict()
status = {"0": "✅", "1": "❌", "2": "⛔️"}

def gen_chapter_status(user_chapter_config):
    if not user_chapter_config[0]:
        over_status = status["1"]
    elif not user_chapter_config[1]:
        over_status = status["0"]
    else:
        over_status = status["2"]    
    return over_status

def gen_topic_status(topic,selected_topic_list):
    if topic in selected_topic_list:
        topic_status = status["0"]
    else:
        topic_status = status["1"]
    return topic_status

def gen_pre_next_page(chapter_id):
    chapter_list = list(chapter_dict.keys())
    chap_num = chapter_list.index(chapter_id)  # 获取用户选取的topic
    if chap_num == 0:
        prev_chap = chapter_list[0]
    if chap_num == len(chapter_list) - 1:
        next_chap = chapter_list[0]
    if chap_num > 0:
        prev_chap = chapter_list[chap_num - 1]
    if chap_num < len(chapter_list) - 1:
        next_chap = chapter_list[chap_num + 1]
    return chap_num, prev_chap, next_chap

def set_user_topic_config(uid,chapter_id,topic_index,topic_status):
    topic_list = get_user_topic_config(uid,chapter_id)
    topic= list(chapter_dict[chapter_id].keys())
    if topic_status == status["0"]:
        topic_list[0].remove(topic[int(topic_index)])
        topic_list[1].append(topic[int(topic_index)])
        set_user_config(uid, chapter_id, topic_list)
    if topic_status == status["1"]:
        topic_list[1].remove(topic[int(topic_index)])
        topic_list[0].append(topic[int(topic_index)])
        set_user_config(uid, chapter_id, topic_list)

def set_user_chapter_config(uid,chapter_id,overall_status):
    chapter_list =get_user_chapter_config(uid)
    if overall_status == status["0"]:
        set_user_config(uid, chapter_id,
                    [list(), list(chapter_list.keys())])
    if overall_status == status["1"] or overall_status == status["2"]:
        set_user_config(uid, chapter_id,
                        [list(chapter_list.keys()), list()])

def update_chapter_list(user_id):  # 更新章节列表和按钮
    menu_keyboard = []
    chapter_preview_msg = "Chapter List\n\n"
    count = 1
    chapter_list = get_chapter_list(user_id)       
    for key, value in chapter_list.items():
        over_status = gen_chapter_status(value)
        chapter_preview_msg += f"{count} {key} {over_status}\n"
        menu_keyboard.append([
            InlineKeyboardButton(
                text=f"{count} {over_status}", callback_data=f"custom-select:{key}:{over_status}:{user_id}"),
            InlineKeyboardButton(
                text=f"Choose {count} Topic", callback_data=f"custom-topic:{key}:{over_status}:{user_id}")
        ])
        count += 1

    menu_keyboard.append([
        InlineKeyboardButton(
            text=f"Finish", callback_data=f"custom-finish:{user_id}")
    ])
    return chapter_preview_msg, menu_keyboard


def update_topic_list(chapter_id, user_id):
    topic_list = list(chapter_dict[chapter_id].keys())  # 获取数据库中的所有topic列表
    selected_topic_list = get_user_topic_config(user_id,chapter_id)[0]
    topic_status_list = ""
    chap_num,prev_chap, next_chap = gen_pre_next_page(chapter_id)
    topic_preview_msg = f"Topic List\nChapter Name:{chapter_id}\n\n"
    topic_menu_keyboard = []
    count = 1
    for topic in topic_list:
        topic_index = topic_list.index(topic)
        topic_status = gen_topic_status(topic,selected_topic_list)
        topic_preview_msg += f"{count} {topic} {topic_status}\n"
        topic_status_list += f"{topic_index}-{topic_status},"
        topic_menu_keyboard.append([
            InlineKeyboardButton(
                text=f"{count} {topic_status}", callback_data=f"topic-select:{chapter_id}:{topic_index}:{topic_status}:{user_id}")
        ])
        count += 1
    topic_menu_keyboard.append([
        InlineKeyboardButton(
            text=f"Prev", callback_data=f"topic-page:{prev_chap}:{user_id}"),
        InlineKeyboardButton(text=f"Back to Chapter List",
                            callback_data=f"topic-back:{chap_num}:{topic_status_list}:{user_id}"),
        InlineKeyboardButton(
            text=f"Next", callback_data=f"topic-page:{next_chap}:{user_id}")
    ])
    return topic_preview_msg, topic_menu_keyboard


@check_chatid_filter
def custom_chapter_command(update: Update, context: CallbackContext) -> None:
    incoming_message = update.effective_message
    user_id = incoming_message.from_user.id
    chapter_preview_msg, menu_keyboard = update_chapter_list(str(user_id))
    incoming_message.reply_markdown_v2(
        text=chapter_preview_msg, reply_markup=InlineKeyboardMarkup(menu_keyboard))


@check_chatid_filter
@check_callback_user
def handle_menu_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <= 1:
        return
    if data[0] == "custom-select":
        set_user_chapter_config(data[-1],data[1],data[-2])
        chapter_preview_msg, menu_keyboard = update_chapter_list(data[-1])
        query.edit_message_text(text=chapter_preview_msg,
                                reply_markup=InlineKeyboardMarkup(menu_keyboard))

    if data[0] == "custom-topic":
        topic_preview_msg, topic_menu_keyboard = update_topic_list(
            data[1], data[-1])
        query.edit_message_text(
            text=topic_preview_msg, reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))

    if data[0] == "custom-finish":
        filename = f"{ENV.DATA_DIR}/user_chapter_dict.json"
        update_data_to_file(data[-1], filename)
        display_data = display_user_config(data[-1])
        query.edit_message_text(
            text=f"设置已保存!\n您所选择的设置为\n{str(display_data)}\n\n请使用/m开始游戏!\n\n您也可以使用/c再次更改您的设置")


@check_chatid_filter
@check_callback_user
def handle_topic_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(":")
    if len(data) <= 2:
        return
    if data[0] == "topic-select":
        set_user_topic_config(data[-1],data[1],data[2],data[-2])
        topic_preview_msg, topic_menu_keyboard = update_topic_list(
            data[1], data[-1])
        query.edit_message_text(
            text=topic_preview_msg, reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))
    if data[0] == "topic-page":
        if data[1] != "None":
            topic_preview_msg, topic_menu_keyboard = update_topic_list(
                data[1], data[-1])
            query.edit_message_text(
                text=topic_preview_msg, reply_markup=InlineKeyboardMarkup(topic_menu_keyboard))
    if data[0] == "topic-back":
        chapter_preview_msg, menu_keyboard = update_chapter_list(data[-1])
        query.edit_message_text(text=chapter_preview_msg,
                                reply_markup=InlineKeyboardMarkup(menu_keyboard))


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("c", custom_chapter_command))

    dp.add_handler(CallbackQueryHandler(
        handle_menu_callback, pattern="^custom-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    dp.add_handler(CallbackQueryHandler(
        handle_topic_callback, pattern="^topic-[A-Za-z0-9_]*:[A-Za-z0-9_]*"))
    return [BotCommand("c", "configure chapter and topic you want to play")]
