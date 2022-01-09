
from re import U
from utils.fileproc import read_file_to_dict
from dict.picture_dict import chapter_dict,word_dict
from config import ENV
import json,os
stored_data = {}

def check_user_config_file():
    try:
        if not os.path.exists(f"{ENV.DATA_DIR}/user_chapter_dict.json"):
            with open(f"{ENV.DATA_DIR}/user_chapter_dict.json", 'x') as fp:
                pass
        return True
    except Exception as e:
        return False  
    

def gen_user_chapter_dict(uid):
    fetch_user_data(uid)
    if not stored_data: #如果stored_data是空的，就根据chapter_dict重新生成stored_data
        stored_data[uid] = {}
        for key,val in chapter_dict.items():
            stored_data[uid][key] = []
            stored_data[uid][key].append(list(val.keys()))
            stored_data[uid][key].append(list())
    return stored_data



def fetch_user_data(uid):
    global stored_data
    user_chapter_dict = read_file_to_dict(f"{ENV.DATA_DIR}/user_chapter_dict.json")
    if user_chapter_dict:
        if uid in list(user_chapter_dict.keys()) and user_chapter_dict[uid]:
            for key,value in user_chapter_dict[uid].items():
                #和chapter_dict比较，如果chapter_dict里面没有这个key，就把这个key删除
                if key not in list(chapter_dict.keys()):
                    user_chapter_dict[uid].pop(key)
                for item in value[0]:
                    if item not in list(chapter_dict[key].keys()):
                        user_chapter_dict[uid][key][0].remove(item)
                for item in value[1]:
                    if item not in list(chapter_dict[key].keys()):
                        user_chapter_dict[uid][key][1].remove(item)            
            stored_data[uid] = user_chapter_dict[uid]
            return stored_data
    return None

def update_data_to_file(uid,filename):
    global stored_data
    try:
        check_user_config_file()
        user_chapter_dict = read_file_to_dict(f"{ENV.DATA_DIR}/user_chapter_dict.json")
        if not user_chapter_dict:
            user_chapter_dict = {}
        user_chapter_dict[uid] = {}
        for key,value in stored_data[uid].items():
            user_chapter_dict[uid][key] = value
        user_chapter_dict = json.dumps(user_chapter_dict)
        with open(filename,"w") as f:
                f.write(f"{user_chapter_dict}")
        return True
    except Exception as e:
        print(e)
        return False

def set_user_config(uid,chapter_id,data):
    #data format:
    try:
        stored_data[uid][chapter_id] = data
        return True
    except Exception as e:
        print(e)
        return False

def get_user_word_dict(uid):
    if stored_data[uid] == None:
        return word_dict
    else:
        user_word_dict = {}
        for key, value in word_dict.items():
            if value[0]["topic"] in stored_data[uid][value[0]["chapter"]][0]:
                user_word_dict[key] = value
        return user_word_dict

def clear_user_config(uid):
    stored_data.pop(uid)
    return True
