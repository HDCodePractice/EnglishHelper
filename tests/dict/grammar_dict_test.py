from dict import grammar_dict


def test_get_grammar_list():
    grammar_list = grammar_dict.get_grammar_list()
    assert len(grammar_list) > 0
    assert 'Past Continuous' in grammar_list


def test_get_grammar():
    assert len(grammar_dict.get_grammar('Past Continuous')) > 0
    assert grammar_dict.get_grammar('papapa') is None


def test_check_extra_dict(shared_datadir):
    assert grammar_dict.check_extra_dict(shared_datadir) == 0


def test_get_grammar_button_list():
    assert len(grammar_dict.get_grammar_button_list("gram:")) > 0
