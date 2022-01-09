from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def test_gen_chapter_list():
    from cmdproc.preview_cmd import gen_chapter_list
    user_id= "12345"
    chapter_msg,kb = gen_chapter_list(user_id)
    assert chapter_msg == "Chapter List\n\n"
    assert kb[0][0].callback_data == "preview-chapter-topic:Computer:12345"

def test_gen_topic_list():
    from cmdproc.preview_cmd import gen_topic_list
    chapter_id = "Computer"
    user_id = "12345"
    topic_msg,kb = gen_topic_list(chapter_id,user_id)
    assert topic_msg == "Topic List\nChapter Name:Computer\n\n1 Program\n"
    assert kb[0][0].callback_data == "preview-topic-page:None:12345"