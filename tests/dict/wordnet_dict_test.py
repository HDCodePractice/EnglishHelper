from config import ENV
from nltk.corpus import wordnet as wn

from dict import wordnet_dict


def test_dict(shared_datadir):
    ENV.NLTK_DATA_DIR = f"{shared_datadir}/wordnet"
    wordnet_dict.download_wordnet()
    d = wordnet_dict.dict("dog")
    assert d.find("noun") == 0
    d = wordnet_dict.dict("look")
    # print(d)
    assert d.find("noun:") == 0
    assert d.find("verb:") > 0


def test_get_definition_examples(shared_datadir):
    ENV.NLTK_DATA_DIR = f"{shared_datadir}/wordnet"
    wordnet_dict.download_wordnet()
    d = wordnet_dict.get_definition_examples("like", pos=wn.NOUN)
    # assert d.find("noun") == 0
    d = wordnet_dict.get_definition_examples("look", pos=wn.VERB)
    print(d)
    # assert d.find("verb") == 0
