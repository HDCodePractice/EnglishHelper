from json import load

from config import ENV
from dict import grammar_dict
from telegram import BotCommand, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
from utils.filters import check_chatid_filter


@check_chatid_filter
def rgrammar_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer("let's go...")
    g = query.data.split(":")[1]
    msg = grammar_dict.get_grammar(g)
    buttons = grammar_dict.get_grammar_button_list(
        "gram:", exclude=[g])
    query.edit_message_text(text=msg, parse_mode="MarkdownV2",
                            reply_markup=InlineKeyboardMarkup(buttons))


@check_chatid_filter
def grammar_command(update: Update, context: CallbackContext) -> None:
    buttons = grammar_dict.get_grammar_button_list("gram:")
    update.effective_message.reply_text(
        "English is simple,remeber **S**\(subject\)**V**\(verb\)[**O**\(object\)]",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=False, parse_mode="MarkdownV2"
    )


def add_dispatcher(dp):
    dp.add_handler(CommandHandler("g", grammar_command))
    dp.add_handler(CallbackQueryHandler(
        rgrammar_callback, pattern="^gram:[A-Za-z0-9_]*"))
    return [BotCommand("g", "My Grammar Book")]
