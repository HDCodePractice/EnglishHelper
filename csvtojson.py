import csv
from utils.fileproc import save_word_dict, gen_pic_json_from_csv
from pybadges import badge

word_dict= {}

with open('iverbs.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # row格式为: {'Base Form': 'wring', 'Simple Past': 'wrung', 'Past Participle': 'wrung', 'Chinese': '拧', '': ''}
        d = "Irregular Verbs: " 
        for key, value in row.items():
            # 将row 变为 d格式 : awake awoke awoken 苏醒
            if value != "":
                d += f"{value} "
        for key, value in row.items():
            if key not in ['','Chinese']: 
                words = value.split('/')  # 处理 burn burned/burnt burned/burnt
                for word in words:
                    # 将单词说明添加到word_dict中
                    if word not in word_dict:   # 如果单词不在word_dict中
                        word_dict[word] = [d]
                    else:
                        if d not in word_dict[word]: # 如果单词在word_dict中，但是说明不在word_dict[word]中
                            word_dict[word].append(d)

with open('inouns.csv','r') as csvnounfile:
    reader = csv.DictReader(csvnounfile)
    for row in reader:
        # row格式为: {'singular': 'calf', 'plural': 'calves', 'Chinese': '小牛'}
        g = "Irregular Plural Nouns: "
        for key, value in row.items():
            # 将row 变为 d格式 : calf calves 小牛
            if value != "":
                g += f"{value} "
        for key, value in row.items():
            if key not in ['','Chinese']:
                words = value.split('/') 
                for word in words:
                    # 将单词说明添加到word_dict中
                    if word not in word_dict:
                        word_dict[word] = [g]
print(f"Irregular单词条目：{len(word_dict)}个")
save_word_dict("word_dict.json",word_dict)
s = badge(left_text="Irregular Words",right_text=f"{len(word_dict)}")
with open('irregular.svg', 'w') as f:
    f.write(s)

word_dict={}
chapter_dict={}

with open('res/picwords.csv','r') as csvfile:
    gen_pic_json_from_csv(csvfile)