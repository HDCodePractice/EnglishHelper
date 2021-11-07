import csv
from json import dump

word_dict= {}

def save_word_dict():
    with open("word_dict.json", 'w') as configfile:
        dump(word_dict, configfile, indent=2,ensure_ascii=False)

with open('iverbs.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # row格式为: {'Base Form': 'wring', 'Simple Past': 'wrung', 'Past Participle': 'wrung', 'Chinese': '拧', '': ''}
        d = "Irregular Verbs:" 
        for key, value in row.items():
            # 将row 变为 d格式 : awake awoke awoken 苏醒
            if value != "":
                d += f"{value} "
        for key, value in row.items():
            if key not in ['','Chinese']:
                words = value.split('/')
                for word in words:
                    # 将单词说明添加到word_dict中
                    if word not in word_dict:   # 如果单词不在word_dict中
                        word_dict[word] = [d]
                    else:
                        if d not in word_dict[word]: # 如果单词在word_dict中，但是说明不在word_dict[word]中
                            word_dict[word].append(d)
save_word_dict()