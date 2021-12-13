
from utils.fileproc import read_file_to_dict
from dict.picture_dict import chapter_dict,word_dict
import json
stored_data = {}

def gen_user_chapter_dict(uid):
    stored_data=fetch_user_data(uid)
    if stored_data == None: #如果stored_data是空的，就根据chapter_dict重新生成stored_data
        for key,val in chapter_dict.items():
            stored_data[uid][key] = []
            stored_data[uid][key].append(list(val.keys()))
            stored_data[uid][key].append(list())
    return stored_data


def fetch_user_data(uid):
    user_chapter_dict = read_file_to_dict("user_chapter_dict.json")
    if user_chapter_dict:
        if uid in list(user_chapter_dict.keys()) and user_chapter_dict[uid]:
            stored_data[uid] = user_chapter_dict[uid]
            return stored_data
    return None

def update_data_to_file(uid,filename):
    try:
        user_chapter_dict = read_file_to_dict("user_chapter_dict.json")
        for key,value in stored_data[uid].items():
            user_chapter_dict[uid][key] = value
        user_chapter_dict = json.dumps(user_chapter_dict)
        with open(filename,"w") as f:
                f.write(f"{user_chapter_dict}")
        return True
    except Exception as e:
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
