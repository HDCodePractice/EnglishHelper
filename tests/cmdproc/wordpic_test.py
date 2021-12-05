def test_check_answer():
    from cmdproc.wordpic import check_answer
    assert check_answer("slash", "5", "hd001") == True
    assert check_answer("slasha", "5", "hd001") == False
    assert check_answer("5", "slasha", "hd001") == False
