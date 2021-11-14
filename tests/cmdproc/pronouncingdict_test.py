def test_get_answer():
    from cmdproc.pronouncingdict import get_answer
    # 查不到
    assert get_answer('pronouncingdict')[0] == '在库存中没有找到这个单词的发音规则，去浩瀚的互联网查询吧～'
    # 查到的相关拼读少于20
    assert get_answer('pronouncing')[0] == """pronouncing
1. [P R AH0 N AW1 N S IH0 NG]
announcing bouncing denouncing mispronouncing pouncing renouncing trouncing\n\n"""
    # 查到的相关拼读多于20
    assert get_answer('read')[0] != get_answer('read')[0]