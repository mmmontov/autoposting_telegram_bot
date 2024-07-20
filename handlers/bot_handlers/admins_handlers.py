import asyncio
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from pydantic import ValidationError
from aiogram.exceptions import TelegramBadRequest

from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS
from services.handlers_functions import get_active_channel_post, format_main_menu_text
from services.database_management import BotDatabase
from config_data.config import load_config
from keyboards.post_actions_keyboard import *
from handlers.bot_handlers.callback_handlers import get_autoposting

router = Router()

config = load_config()

AUTOPOSTING = {
    'mode': False,
    'seconds_delay': 600
} 


# on/off autoposting (вкл/выкл автоотправку постов)
@router.message(Command(commands='switch_autoposting'))
async def switch_autoposting(message: Message):
    global AUTOPOSTING
    delay = AUTOPOSTING['seconds_delay']
    # включение и выключение непрерывнго выполнения по кнопке
    AUTOPOSTING['mode'] = not AUTOPOSTING['mode']
    mode = AUTOPOSTING['mode']
    await message.answer(f'автопостинг - {mode}')
    print('автопостинг', mode)
    
    while AUTOPOSTING['mode']:   
        await asyncio.sleep(delay)
        if AUTOPOSTING['mode']:
            await get_active_channel_post(message)               
  
        
# get recipe (запросить случайный рецепт)  
@router.message(Command(commands='get_post'))
async def get_post(message: Message):
    await get_active_channel_post(message)
    
    
# get bot menu (главное меню бота)
@router.message(Command(commands='bot_menu'))
async def get_bot_menu(message: Message):
    text = format_main_menu_text(get_autoposting())
    await message.answer(text=text, 
                         reply_markup=create_main_menu_kb())

