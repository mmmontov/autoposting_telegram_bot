import asyncio
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from pydantic import ValidationError
from aiogram.exceptions import TelegramBadRequest

from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS
from parsing.recipes_parsing.chief_tm_parsing import gather_recipe
from services.handlers_functions import get_recipe


router = Router()

AUTOPOSTING = {
    'mode': False,
    'seconds_delay': 10
} 


# on/off autoposting (вкл/выкл автоотправку постов)
@router.message(Command(commands='switch_autoposting'))
async def switch_autoposting(message: Message):
    global AUTOPOSTING
    delay = AUTOPOSTING['seconds_delay']
    # включение и выключение непрерывнго выполнения по кнопке
    AUTOPOSTING['mode'] = not AUTOPOSTING['mode']
    mode = AUTOPOSTING['mode']
    print('автопостинг', mode)
    
    while AUTOPOSTING['mode']:   
        await asyncio.sleep(delay)
        if AUTOPOSTING['mode']:
            await get_recipe(message)               
  
        
# get recipe (запросить случайный рецепт)  
@router.message(Command(commands='get_post'))
async def get_post(message: Message):
    await get_recipe(message)