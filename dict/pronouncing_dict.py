import random

import pronouncing


def get_rhyme(p):
    """
    Returns the rhyme of the pronouncing.
    """
    return [w for w in pronouncing.rhyme_lookup.get(pronouncing.rhyming_part(p), [])
            if w != p]


def get_pronouncing(word):
    """
    Returns the pronunciation of the word.
    """
    reslt = []
    ps = pronouncing.phones_for_word(word)
    for p in ps:
        reslt.append([p, get_rhyme(p)])
    return reslt


def dict(word):
    """
    Returns the definition of the word.
    """
    reslt = get_pronouncing(word)
    if len(reslt) == 0:
        return ""
    msg = ""
    count = 1
    for p in reslt:
        msg += f"{count}. [{p[0]}]\n"
        near = [w for w in p[1] if w != word]
        if len(near) > 10:
            near = random.sample(near, 10)
        for r in near:
            msg += f"{r} "
        msg = f"{msg[:-1]}\n\n"
        count += 1
    return msg[:-2]
