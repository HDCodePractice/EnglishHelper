from config import ENV

from dict.wordnet_dict import dict, download_wordnet


def test_dict():
    ENV.NLTK_DATA_DIR = "wordnet"
    download_wordnet()
    d = dict("dog")
    # print(d)
    assert d.find("noun") == 0
    assert d.find("informal term for a man") > 0
    assert d.find("metal supports for logs in a fireplace") > 0
    assert d.find("verb:") > 0
