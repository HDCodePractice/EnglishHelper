from dict import pronouncing_dict


def test_dict():
    # 查不到
    assert pronouncing_dict.dict('pronouncingdict') == ''
    # 查到的相关拼读少于20
    assert pronouncing_dict.dict('pronouncing') == """1. [P R AH0 N AW1 N S IH0 NG]
announcing bouncing denouncing mispronouncing pouncing renouncing trouncing"""
    # 查到的相关拼读多于20
    assert pronouncing_dict.dict('read') != pronouncing_dict.dict('read')
    # 查出一句话的音标
    assert pronouncing_dict.dict('i am god') == "AY1 . AE1 M . G AA1 D"
    # 测试一句话的标点符号
    assert pronouncing_dict.dict('I am god!') == "AY1 . AE1 M . G AA1 D"
