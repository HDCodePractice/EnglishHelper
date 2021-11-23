from dict import pronouncing_dict


def test_dict():
    # 查不到
    assert pronouncing_dict.dict('pronouncingdict') == ''
    # 查到的相关拼读少于20
    assert pronouncing_dict.dict('pronouncing') == """1. [P R AH0 N AW1 N S IH0 NG]
announcing bouncing denouncing mispronouncing pouncing renouncing trouncing"""
    # 查到的相关拼读多于20
    assert pronouncing_dict.dict('read') != pronouncing_dict.dict('read')
