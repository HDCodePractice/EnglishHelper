def test_get_answer():
    from cmdproc.pronouncingdict import get_answer
    # 查不到
    assert get_answer('pronouncingdict')[0] == 'pronouncingdict:\n\nGo to the vast Internet and look it up~'
    # 查到的相关拼读少于20
    assert get_answer('pronouncing')[0] == """pronouncing:
1. [P R AH0 N AW1 N S IH0 NG]
announcing bouncing denouncing mispronouncing pouncing renouncing trouncing\n\n"""
    # 查到的相关拼读多于20
    assert get_answer('read')[0] != get_answer('read')[0]