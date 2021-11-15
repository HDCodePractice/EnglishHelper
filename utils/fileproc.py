from json import dump
import csv

def save_word_dict(filename,words_dict):
    with open(filename, 'w') as configfile:
        dump(words_dict, configfile, indent=2,ensure_ascii=False)

def gen_pic_json_from_csv(csvfile,out_path="./"):
    word_dict={}
    chapter_dict={}

    reader = csv.DictReader(csvfile)
    for row in reader:
        # row格式为：{'File Name': '86.jpg', 'Chapter': 'Clothing', 'Topic': 'Everyday Clothes', 'words': '1.shirt|2.jeans|3.dress|4.T-shirt|5.baseball cap|6.socks|7.athletic shoes|A.tie|8.blouse|9.handbag|10.skirt|11.suit|12.slacks/pants|13.shoes|14.sweater|B.put on'}
        filename = row['File Name']
        filenumber = filename.split('.')[0]
        chapter = row['Chapter']
        topic = row['Topic']
        words = row['words']
        for word in words.split('|'):  # 切出所有的带number的单词
            num , pre_word = word.split('.')  # 切出number和单词
            for word in pre_word.split('/'):    # 一个图有多个单词会使用/分割
                # 将单词说明添加到word_dict中
                if word not in word_dict:   # 如果单词不在word_dict中
                    word_dict[word.lower()] = [{'chapter':chapter,'topic':topic,'filename':filename,'number':num}]
                else:
                    word_dict[word.lower()].append({'chapter':chapter,'topic':topic,'filename':filename,'number':num})
                # 将单词说明添加到chapter_dict中
                if chapter not in chapter_dict:
                    chapter_dict[chapter] = {}
                if topic not in chapter_dict[chapter]:
                    chapter_dict[chapter][topic] = {}
                if filenumber not in chapter_dict[chapter][topic]:
                    chapter_dict[chapter][topic][filenumber] = {}
                if num not in chapter_dict[chapter][topic][filenumber]:
                    chapter_dict[chapter][topic][filenumber][num] = [word]
                if word not in chapter_dict[chapter][topic][filenumber][num]:
                    chapter_dict[chapter][topic][filenumber][num].append(word)

    print(f"看图识词单词条目：{len(word_dict)}个")
    save_word_dict(f"{out_path}pic_dict.json",word_dict)
    save_word_dict(f"{out_path}chapter_dict.json",chapter_dict)