import asyncio
import schedule
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from pydantic import ValidationError


from create_bot import bot
from config_data.config import load_config, get_active_channel, channels
from services.database_management import BotDatabase
from parsing.recipes_parsing.recipes_functions import get_recipe
from parsing.facts_parsing.facts_functions import get_fact


config = load_config()

channels_dict = {
    'recipes': {
        'id': channels[0],
        'schelude': ['15:00', '19:00', '22:00', '00:00', '02:00'],
        'parser': get_recipe
    },
    'facts': {
        'id': channels[1],
        'schelude': ['14:00', '17:00', '20:00', '00:00'],
        'parser': get_fact
    }
}


# ==== create name:parser dict and return post in active channel theme =======

parsers = [channels_dict[channel]['parser'] for channel in channels_dict] # распологать в том порядке, в котором id каналов в env
channels_parers = {
    name: pars for name, pars in zip(config.tg_channel.channel_names, parsers)
}

async def get_active_channel_post(message: Message):
    active_channel = get_active_channel()
    return await channels_parers[active_channel](message)

# ============================================================================


# =========== start/stop autoposting schelude ================================

recipes_schelude = channels_dict['recipes']['schelude']
facts_schelude = channels_dict['facts']['schelude']
        
async def publick_next_queue_post(channel):
    db = BotDatabase(config.database.path)
    try:
        id, text, photo = db.get_next(channel=channel)
        await bot.send_photo(channel, caption=text, photo=photo)
    except TypeError:
        print('посты закончились')
    
# так называемый костыль, который соединяет синхронность с асинхронностью
def schedule_send_recipe():
    asyncio.ensure_future(publick_next_queue_post(channels_dict['recipes']['id']))

def schelude_send_fact():
    asyncio.ensure_future(publick_next_queue_post(channels_dict['facts']['id']))

# старт очереди
async def start_queue():
    # schedule.every(5).seconds.do(schedule_send_post)
    for time in recipes_schelude:
        schedule.every().day.at(time).do(schedule_send_recipe)
    for time in facts_schelude:
        schedule.every().day.at(time).do(schelude_send_fact)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
         
async def stop_queue():
    return schedule.clear()

# ============================================================================



# =============== formating texts in posts ===================================

def format_main_menu_text(post_mode):
    db = BotDatabase(config.database.path)
    queue_posts_count = len(db.get_queue())
    posting = 'включен 👍' if post_mode else 'выключен 👎'
    
    text = f'''актинвый канал - {get_active_channel()}\n
автопостинг - <b>{posting}</b>\n
постов в очереди - <b>{queue_posts_count}</b>'''
    return text

# 👍👎