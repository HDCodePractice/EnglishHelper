import csv
from json import dump

word_dict= {}

def save_word_dict(filename):
    with open(filename, 'w') as configfile:
        dump(word_dict, configfile, indent=2,ensure_ascii=False)

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
print(f"单词条目：{len(word_dict)}个")
save_word_dict("word_dict.json")

word_dict={}

with open('picwords.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # row格式为：{'File Name': '86.jpg', 'Chapter': 'Clothing', 'Topic': 'Everyday Clothes', 'words': '1.shirt|2.jeans|3.dress|4.T-shirt|5.baseball cap|6.socks|7.athletic shoes|A.tie|8.blouse|9.handbag|10.skirt|11.suit|12.slacks/pants|13.shoes|14.sweater|B.put on'}
        filename = row['File Name']
        chapter = row['Chapter']
        topic = row['Topic']
        words = row['words']
        for word in words.split('|'):  # 切出所有的带number的单词
            num , pre_word = word.split('.')  # 切出number和单词
            for word in pre_word.split('/'):    # 一个图有多个单词会使用/分割
                if word not in word_dict:   # 如果单词不在word_dict中
                    word_dict[word.lower()] = [{'chapter':chapter,'topic':topic,'filename':filename,'number':num}]
                else:
                    word_dict[word.lower()].append({'chapter':chapter,'topic':topic,'filename':filename,'number':num})

print(f"单词条目：{len(word_dict)}个")
save_word_dict("pic_dict.json")