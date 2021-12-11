import os

from config import ENV


def test_reload_dict(shared_datadir):
    os.chdir(shared_datadir)
    ENV.DATA_DIR = f"{shared_datadir}/ext"
    from dict import picture_dict
    picture_dict.reload_dict()
    print(picture_dict.word_dict)
    print(picture_dict.word_dict['test1'])
