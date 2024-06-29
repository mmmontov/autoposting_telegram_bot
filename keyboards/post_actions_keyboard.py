from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import CALLBACK_RU

def create_post_actions_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(*[InlineKeyboardButton(text=txt, callback_data=cd) 
                     for cd, txt in CALLBACK_RU.items()],
        width=1
    )
    return kb_builder.as_markup()


    