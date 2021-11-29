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
    # print(d)
    assert d.find("a similar kind") > 0
    d = wordnet_dict.get_definition_examples("look", pos=wn.VERB)
    # print(d)
    assert d.find("perceive with attention") > 0


def test_get_synonyms_antonyms(shared_datadir):
    ENV.NLTK_DATA_DIR = f"{shared_datadir}/wordnet"
    wordnet_dict.download_wordnet()
    d = wordnet_dict.get_synonyms_antonyms("like")
    # print(d)
    assert len(d[0]) > 0
    assert len(d[1]) > 0
    d = wordnet_dict.get_synonyms_antonyms_msg("like")
    assert d.find("Synonyms:") == 0
    assert d.find("Antonyms:") > 0
    d = wordnet_dict.get_synonyms_antonyms_msg("like", wn.synset("like.n.01"))
    # print(d)
    assert d.find("Synonyms:") > 0
    d = wordnet_dict.get_synonyms_antonyms_msg("like", wn.synset("wish.v.02"))
    # print(d)
    assert d.find("Synonyms:") > 0
