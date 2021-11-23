import random
from pathlib import Path

import nltk
from config import ENV
from nltk.corpus import wordnet as wn


def download_wordnet():
    print(ENV.NLTK_DATA_DIR)
    if ENV.NLTK_DATA_DIR is None:
        nltk.download("wordnet")
    else:
        Path(ENV.NLTK_DATA_DIR).mkdir(parents=True, exist_ok=True)
        nltk.data.path.append(ENV.NLTK_DATA_DIR)
        nltk.download("wordnet", download_dir=ENV.NLTK_DATA_DIR)


def get_synonyms_antonyms(word):
    synonyms = {word}
    antonyms = {word}
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.add(l.antonyms()[0].name().replace("_", " "))
            else:
                synonyms.add(l.name().replace("_", " "))
    synonyms.remove(word)
    antonyms.remove(word)
    return list(synonyms), list(antonyms)


def get_synonyms_antonyms_msg(word):
    synonyms, antonyms = get_synonyms_antonyms(word)
    msg = ""
    if len(synonyms) > 0:
        msg += f"Synonyms: \n{', '.join(synonyms)}\n\n"
    if len(antonyms) > 0:
        msg += f"Antonyms: \n{', '.join(antonyms)}\n\n"
    return msg[:-2]


def get_definition_examples(word, pos):
    ws = wn.synsets(word, pos=pos)
    d = ""
    count = 1
    for w in ws:
        d += f"{count}. {w.definition()}\n"
        if len(w.examples()) > 0:
            examples = w.examples()
            e = random.choice(examples)
            if e[-1] in ["?", "!"]:
                d += f"E: {e}\n"
            else:
                d += f"E: {e}.\n"
        count += 1
        if count > 5:
            break
    return d[:-1]


def dict(word):
    description = ""
    d = get_definition_examples(word, pos=wn.NOUN)
    if len(d) > 0:
        description += f"noun:\n{d}\n\n"
    d = get_definition_examples(word, pos=wn.VERB)
    if len(d) > 0:
        description += f"verb:\n{d}\n\n"
    d = get_definition_examples(word, pos=wn.ADJ)
    if len(d) > 0:
        description += f"adj:\n{d}\n\n"
    d = get_definition_examples(word, pos=wn.ADV)
    if len(d) > 0:
        description += f"adv:\n{d}\n\n"

    return description[:-1]
