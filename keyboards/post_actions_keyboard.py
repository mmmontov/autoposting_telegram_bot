from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import CALLBACK_RU
from services.database_management import BotDatabase
from config_data.config import load_config

config = load_config()

def create_inline_kb(dict: dict, layout: list[int]=[]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    items = iter(dict.items())

    # итерируемся по числам которые обозначают кол-во кнопок в ряду
    for width in layout:
        bttns = []
        for _ in range(width):
            try:
                cd, txt = next(items)
                bttns.append(InlineKeyboardButton(text=txt, callback_data=cd))
            except StopIteration: 
                pass
        kb_builder.row(*bttns, width=width)
    
    # оставшиеся добавляем по одной в ряд
    rest = list(items)
    if rest:
        kb_builder.row(*[InlineKeyboardButton(text=txt, callback_data=cd) 
                        for cd, txt in rest], width=1)
    return kb_builder.as_markup()

# ======================= main callbacks ======================================

def create_post_actions_kb() -> InlineKeyboardMarkup:
    return create_inline_kb(CALLBACK_RU['main_actions'], [1, 1, 2, 1])


def create_edit_post_kb() -> InlineKeyboardMarkup:
    return create_inline_kb(CALLBACK_RU['edit_menu'], [2, 1])


def create_main_menu_kb() -> InlineKeyboardMarkup:
    return create_inline_kb(CALLBACK_RU['main_menu'], [1, 2, 1, 1])
    
    
def create_bot_mode_menu() -> InlineKeyboardMarkup:
    return create_inline_kb(CALLBACK_RU['bot_mode'])


# =============================================================================



# ==================== on buttons click =======================================


def create_main_actions_add_to_queue() -> InlineKeyboardMarkup:
    return create_inline_kb(CALLBACK_RU['on_buttons_click']['main_actions_add_to_queue'], 
                            [1, 1, 2, 1])
    