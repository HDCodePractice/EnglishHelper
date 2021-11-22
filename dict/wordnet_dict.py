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


def dict(word):
    description = ""
    ws = wn.synsets(word, pos=wn.NOUN)
    d = ""
    count = 1
    for w in ws:
        d += f"{count}.{w.definition()}\n"
        if len(w.examples()) > 0:
            d += f"E: {random.choice(w.examples())}\n"
        count += 1
        if count > 5:
            break
    if len(d) > 0:
        description += f"noun:\n{d}\n"

    ws = wn.synsets(word, pos=wn.VERB)
    d = ""
    count = 1
    for w in ws:
        d += f"{count}.{w.definition()}\n"
        if len(w.examples()) > 0:
            d += f"E: {random.choice(w.examples())}\n"
        count += 1
        if count > 5:
            break
    if len(d) > 0:
        description += f"verb:\n{d}\n"

    ws = wn.synsets(word, pos=wn.ADJ)
    d = ""
    count = 1
    for w in ws:
        d += f"{count}.{w.definition()}\n"
        if len(w.examples()) > 0:
            d += f"E: {random.choice(w.examples())}\n"
        count += 1
        if count > 5:
            break
    if len(d) > 0:
        description += f"adj:\n{d}\n"

    ws = wn.synsets(word, pos=wn.ADV)
    d = ""
    count = 1
    for w in ws:
        d += f"{count}.{w.definition()}\n"
        if len(w.examples()) > 0:
            d += f"E: {random.choice(w.examples())}\n"
        count += 1
        if count > 5:
            break
    if len(d) > 0:
        description += f"adv:\n{d}\n"

    return description[:-1]
