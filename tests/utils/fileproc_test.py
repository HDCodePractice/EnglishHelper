import pytest

from utils import fileproc


def test_gen_irregular_dict_from_csv(shared_datadir):
    with open(f"{shared_datadir}/ext/res/inouns.csv") as inouns_csvfile:
        with open(f"{shared_datadir}/ext/res/iverbs.csv", 'r') as iverb_csvfile:
            word_dict = fileproc.gen_irregular_dict_from_csv(
                iverb_csvfile, inouns_csvfile)
            assert len(word_dict) == 13


def test_gen_pic_dict_from_csv(shared_datadir):
    with open(f"{shared_datadir}/ext/res/picwords.csv") as csvfile:
        word_dict, chapter_dict = fileproc.gen_pic_dict_from_csv(csvfile)
        assert len(word_dict) == 3
        assert len(chapter_dict) == 1


def test_gen_grammar_dict_from_csv(shared_datadir):
    with open(f"{shared_datadir}/ext/res/grammar.csv") as csvfile:
        word_dict = fileproc.gen_grammar_dict_from_csv(csvfile)
        assert len(word_dict) > 0
