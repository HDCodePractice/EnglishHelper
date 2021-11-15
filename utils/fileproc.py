from json import dump

def save_word_dict(filename,words_dict):
    with open(filename, 'w') as configfile:
        dump(words_dict, configfile, indent=2,ensure_ascii=False)