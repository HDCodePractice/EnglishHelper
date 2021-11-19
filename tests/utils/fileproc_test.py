import pytest
from utils.fileproc import gen_irregular_dict_from_csv
from utils.fileproc import gen_pic_dict_from_csv

def test_gen_irregular_dict_from_csv(shared_datadir):    
    with open(f"{shared_datadir}/inouns.csv") as inouns_csvfile:
        with open(f"{shared_datadir}/iverbs.csv", 'r') as iverb_csvfile:
            word_dict=gen_irregular_dict_from_csv(iverb_csvfile,inouns_csvfile)
            assert len(word_dict) == 13

def test_gen_pic_dict_from_csv(shared_datadir):
    with open(f"{shared_datadir}/picwords.csv") as csvfile:
        word_dict,chapter_dict = gen_pic_dict_from_csv(csvfile)
        assert len(word_dict) == 25
        assert len(chapter_dict) == 1