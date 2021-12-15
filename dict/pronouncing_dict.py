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


def dict(words):
    """
    Returns the definition of the word.
    """
    reslt = []
    msg = ""
    words = words.split()
    for iword in words:
        reslt.append(get_pronouncing(iword))
    if len(reslt[0]) == 0:
        return ""
    if len(reslt) == 1:
        count = 1
        for p in reslt:
            msg += f"{count}. [{p[0][0]}]\n"
            near = [w for w in p[0][1] if w != words[0]]
            if len(near) > 10:
                near = random.sample(near, 10)
            for r in near:
                msg += f"{r} "
            msg = f"{msg[:-1]}\n\n"
            count += 1
        return msg[:-2]
    if len(reslt) > 1:
        for i in range(len(reslt)):
            msg += f"{reslt[i][0][0]} . "
        return msg[:-3]
