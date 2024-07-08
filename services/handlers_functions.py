import asyncio
import schedule
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from pydantic import ValidationError

from parsing.recipes_parsing.chief_tm_parsing import gather_recipe
from keyboards.post_actions_keyboard import create_post_actions_kb
from create_bot import bot
from config_data.config import load_config
from services.database_management import BotDatabase

config = load_config()

posts_schelude = ['13:00', '15:00', '18:00', '20:00', '22:00', '00:00', '02:00']

# recipe get func (функция запрашивает рецепт, проверяет его и отвечает на сообщение)
async def get_recipe(message: Message):
    try:
        post_text, image_url = await gather_recipe()
        # если присутствует текст    
        if post_text:
            # print(post_text)
            await message.answer_photo(photo=image_url, 
                                    caption=post_text, 
                                    reply_markup=create_post_actions_kb())     
            print('рецепт отправлен')
            
    except ValidationError as err:
        print('ошибка в отправке')
        await get_recipe(message)
    except TypeError as err:
        print('ошибка в распаковке')
        await get_recipe(message)
    except TelegramBadRequest:
        print('сообщение слишком длинное') 
        await get_recipe(message)
        
        
async def publick_next_queue_post():
    db = BotDatabase(config.database.path)
    try:
        id, text, photo = db.get_next()
        await bot.send_photo(config.tg_channel.channel_name, caption=text, photo=photo)
    except TypeError:
        print('посты закончились')
    
# так называемый костыль, который соединяет синхронность с асинхронностью
def schedule_send_post():
    asyncio.ensure_future(publick_next_queue_post())

async def start_queue():
    # schedule.every(5).seconds.do(schedule_send_post)
    for time in posts_schelude:
        schedule.every().day.at(time).do(schedule_send_post)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
        
        
async def stop_queue():
    return schedule.clear()