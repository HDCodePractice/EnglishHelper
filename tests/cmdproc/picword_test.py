import pytest

def test_get_show_word():
    from cmdproc.picword import get_show_word
    assert get_show_word("test",0) == "****"
    assert get_show_word("test",1) == "t***"
    assert get_show_word("test",2) == "t**t"
    assert get_show_word("test",3) == "te*t"
    assert get_show_word("test",4) == "test"

def test_check_answer():
    from cmdproc.picword import check_answer
    assert check_answer("3","neck","104") == True
    assert check_answer("3","Neck","104") == True
    assert check_answer("3","Necka","104") == False