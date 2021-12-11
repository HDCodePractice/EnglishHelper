from json import load
from pathlib import Path

from config import ENV
from utils.fileproc import gen_pic_dict_from_csv

word_dict = {}
chapter_dict = {}


def check_extra_dict(dict_dir):
    # 检查是否有用户自定义的单词库
    if dict_dir is None:
        return 0
    try:
        with open(f"{dict_dir}/res/picwords.csv", 'r') as csvfile:
            word_dict, chapter_dict = gen_pic_dict_from_csv(csvfile)
            print(f"看图识词单词条目：{len(word_dict)}个")
            return len(word_dict)
    except FileNotFoundError:
        return 0


def reload_dict():
    global word_dict
    global chapter_dict
    import os
    p = os.getcwd()
    # 加载内置单词库
    with open('pic_dict.json', 'r') as wd:
        word_dict = load(wd)
    with open('chapter_dict.json', 'r') as wd:
        chapter_dict = load(wd)

    # 加载用户自定义单词库
    try:
        with open(f"{ENV.DATA_DIR}/res/picwords.csv", 'r') as csvfile:
            word_dict, chapter_dict = gen_pic_dict_from_csv(
                csvfile, word_dict, chapter_dict)
    except FileNotFoundError:
        pass


if __name__ == 'dict.picture_dict':
    reload_dict()
