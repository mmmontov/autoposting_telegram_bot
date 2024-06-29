import asyncio
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
from pydantic import ValidationError

from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS
from parsing.recipes_parsing.chief_tm_parsing import recipe_parse

router: Router = Router()


# start (старт)
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])
    await message.answer_photo('https://chef.tm/public/pics/175/175654_0.jpg')
    print(message.from_user.id, message.from_user.first_name)
    
    
    
