from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest 
from pydantic import ValidationError

from config_data.config import load_config, get_active_channel
from keyboards.post_actions_keyboard import create_post_actions_kb
from parsing.recipes_parsing.chief_tm_parsing import gather_recipe

config = load_config()


# recipe get func (функция запрашивает рецепт, проверяет его и отвечает на сообщение)
async def get_recipe(message: Message, link=True):
    try:
        post_text, image_url = await gather_recipe()
        # если присутствует текст    
        if post_text:
            if link:
                post_text += f'\n\n{get_active_channel()}'            
            
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
        await get_recipe(message, link=False)