from dict import grammar_dict


def test_get_grammar_list():
    grammar_list = grammar_dict.get_grammar_list()
    assert len(grammar_list) > 0
    assert 'Past Continuous' in grammar_list


def test_get_grammar():
    assert len(grammar_dict.get_grammar('Past Continuous')) > 0
