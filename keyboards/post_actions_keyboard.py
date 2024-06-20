from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import CALLBACK_RU

def create_post_actions_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=CALLBACK_RU['publish_post'],
            callback_data='publish_post'
        ),
        InlineKeyboardButton(
            text=CALLBACK_RU['reject_post'],
            callback_data='reject_post'
        ),
        width=1
    )
    return kb_builder.as_markup()


    