#!/usr/bin/env python3

import json
import os
from environs import Env
from io import StringIO
from dotenv import load_dotenv
import requests
from base64 import b64encode

loads = json.loads
load = json.load
dumps = json.dumps
dump = json.dump

run_path = os.path.split(os.path.realpath(__file__))[0]
config_path = run_path
config_file = ""

CONFIG = {}

def load_config():
    global CONFIG
    with open(config_file, 'r') as configfile:
        CONFIG = load( configfile )
    return CONFIG

def save_config():
    file_dir = os.path.split(config_file)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    with open(config_file, 'w') as configfile:
        dump(CONFIG, configfile, indent=4,ensure_ascii=False)

def get_json():
    return dumps(CONFIG,indent=4,ensure_ascii=False)

def set_default():
    CONFIG.setdefault("Admin",[])       #管理员id
    CONFIG.setdefault("Admin_path","")  #Admin Shell Path
    save_config()

def get_admin_uids():
    if not CONFIG:
        load_config()
    return CONFIG.get("Admin", [])

def get_doppler_env(token):
    token_b64 = b64encode(f"{token}:".encode()).decode()

    url = "https://api.doppler.com/v3/configs/config/secrets/download"

    querystring = {"format":"env"}

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {token_b64}"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return ""

env = Env()
env.read_env(f"{os.getcwd()}/local.env")

doppler_token = env.str('DOPPLER_TOKEN', default='')

if len(doppler_token) > 0 :
    response = get_doppler_env(doppler_token)
    if len(response) > 0:
        config = StringIO(response)
        load_dotenv(stream=config)

class ENV:
    CONTRIBUTORS="贡献者:老房东、lben1216、stephenzhu01、bernieharvard"
    WORKDIR=os.getcwd()
    # BotToken
    BOT_TOKEN = env.str("BOT_TOKEN", default="") 
    # 支持使用Bot的ChatID列表
    CHATIDS = env.list("CHATIDS", [])
    # 管理员ID列表
    ADMIN_IDS = env.list("ADMIN_IDS", [])
    # 存储自定义数据的文件夹
    DATA_DIR = env.str("DATA_DIR", default="/data/user_dict")

if __name__ == "__main__":
    print(ENV.CHATIDS)