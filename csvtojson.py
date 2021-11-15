import csv
from utils.fileproc import save_word_dict, gen_pic_json_from_csv, gen_irregular_dict_from_csv
from pybadges import badge

word_dict= {}

with open('res/iverbs.csv', 'r') as iverb_csvfile:
    with open('res/inouns.csv','r') as inouns_csvfile:
        word_dict=gen_irregular_dict_from_csv(iverb_csvfile,inouns_csvfile)
        print(f"Irregular单词条目：{len(word_dict)}个")
        save_word_dict("word_dict.json",word_dict)
        s = badge(left_text="Irregular Words",right_text=f"{len(word_dict)}")
        with open('irregular.svg', 'w') as f:
            f.write(s)

word_dict={}
chapter_dict={}

with open('res/picwords.csv','r') as csvfile:
    word_dict,chapter_dict = gen_pic_json_from_csv(csvfile)
    print(f"看图识词单词条目：{len(word_dict)}个")
    save_word_dict("pic_dict.json",word_dict)
    save_word_dict("chapter_dict.json",chapter_dict)