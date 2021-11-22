from config import ENV

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
