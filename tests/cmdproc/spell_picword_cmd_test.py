from marshmallow.fields import Number
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def test_get_show_word():
    from cmdproc.spell_picword_cmd import get_show_word
    assert get_show_word("test", 0) == "****"
    assert get_show_word("test", 1) == "t***"
    assert get_show_word("test", 2) == "t**t"
    assert get_show_word("test", 3) == "te*t"
    assert get_show_word("test", 4) == "test"


def test_get_hint_view():
    from cmdproc.spell_picword_cmd import get_hint_view
    msgs = ["第一行", "第二行", "第三行", "第四行"]
    show_count = 1

    number = 0
    filenumber = "1"
    data_word = "abcd / abc"
    words = data_word.split(" / ")

    buttons = [[InlineKeyboardButton(
        "🙏 Click here for a 🔡 🙏", callback_data=f"rhit:{number}:{filenumber}:{data_word}:0")]]
    keyboard = InlineKeyboardMarkup(buttons)
    data = f"rhit:{number}:{filenumber}:{data_word}:0".split(":")
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: a*** / a**\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd / abc:1"
    show_count = 2
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: a**d / a*c\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd / abc:2"
    show_count = 3
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: ab*d / abc\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd / abc:3"
    show_count = 4
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: abcd / abc\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd / abc:4"

    msgs = ["第一行", "第二行", "第三行", "第四行"]
    show_count = 1

    number = 0
    filenumber = "1"
    data_word = "abcd"
    words = data_word.split(" / ")

    buttons = [[InlineKeyboardButton(
        "🙏 Click here for a 🔡 🙏", callback_data=f"rhit:{number}:{filenumber}:{data_word}:0")]]
    keyboard = InlineKeyboardMarkup(buttons)
    data = f"rhit:{number}:{filenumber}:{data_word}:0".split(":")

    show_count = 1
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: a***\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd:1"
    show_count = 2
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: a**d\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd:2"
    show_count = 3
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: ab*d\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd:3"
    show_count = 4
    msg, kb = get_hint_view(msgs, words, show_count,
                            keyboard, data)
    assert msg == "第一行\nHints💡: abcd\n第三行\n第四行"
    assert kb.inline_keyboard[0][0].callback_data == "rhit:0:1:abcd:4"
