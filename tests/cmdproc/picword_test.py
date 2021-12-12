import pytest


def test_get_show_word():
    from cmdproc.spell_picword_cmd import get_show_word
    assert get_show_word("test", 0) == "****"
    assert get_show_word("test", 1) == "t***"
    assert get_show_word("test", 2) == "t**t"
    assert get_show_word("test", 3) == "te*t"
    assert get_show_word("test", 4) == "test"
