from json import load

from config import ENV
from telegram import InlineKeyboardButton
from utils.fileproc import gen_grammar_dict_from_csv

grammar_dict = {}


def check_extra_dict(dict_dir):
    # 检查是否有用户自定义的单词库
    if dict_dir is None:
        return 0
    try:
        with open(f"{ENV.DATA_DIR}/res/grammar.csv", 'r') as csvfile:
            word_dict = gen_grammar_dict_from_csv(
                csvfile)
            print(f"Grammar条目：{len(word_dict)}个")
            return len(word_dict)
    except FileNotFoundError:
        return 0


def reload_dict():
    global grammar_dict
    with open('grammar_dict.json', 'r') as wd:
        grammar_dict = load(wd)
    try:
        with open(f"{ENV.DATA_DIR}/res/grammar.csv", 'r') as csvfile:
            word_dict = gen_grammar_dict_from_csv(
                csvfile,
                grammar_dict)
    except FileNotFoundError:
        pass


reload_dict()


def get_grammar_list():
    return list(grammar_dict.keys())


def get_grammar_button_list(callback_prefix, exclude=""):
    """
    callback_prefix: callback_data回调前缀
    exclude: 不需要列出的语法，可以是list或者str
    """
    gl = get_grammar_list()
    buttons = []
    for g in gl:
        if g == exclude or g in exclude:
            continue
        buttons.append([InlineKeyboardButton(
            g, callback_data=f"{callback_prefix}{g}")])
    return buttons


def get_grammar(name):
    if name in grammar_dict:
        return grammar_dict[name]['description']
    return None
