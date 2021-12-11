
def test_reload_dict(shared_datadir):
    from dict import picture_dict
    picture_dict.reload_dict()
    assert picture_dict.word_dict['test1'] == [
        {'chapter': 'Test_Chapter', 'topic': 'Test_Topic', 'filename': 'test.jpg', 'number': '1'}]
