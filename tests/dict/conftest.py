import pytest
from config import ENV

from dict import wordnet_dict


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def download_wordnet_data(shared_datadir):
    ENV.NLTK_DATA_DIR = f"{shared_datadir}/wordnet"
    wordnet_dict.download_wordnet()
