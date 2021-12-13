from dict import picture_dict


def test_reload_dict(shared_datadir):
    picture_dict.reload_dict()
    assert picture_dict.word_dict['test1'] == [
        {'chapter': 'Test_Chapter', 'topic': 'Test_Topic', 'filename': 'test.jpg', 'number': '1'}]


def test_check_answer():
    assert picture_dict.check_answer("5", "slash", "punctuation1") == True
    assert picture_dict.check_answer("5", "slash", "punctuation1") == True
    assert picture_dict.check_answer("5", "slasha", "punctuation1") == False
