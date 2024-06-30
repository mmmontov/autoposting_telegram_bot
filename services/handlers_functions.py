import asyncio
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from pydantic import ValidationError

from parsing.recipes_parsing.chief_tm_parsing import gather_recipe
from keyboards.post_actions_keyboard import create_post_actions_kb


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