import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest

from services.handlers_functions import start_queue, stop_queue, get_active_channel_post, format_main_menu_text
from keyboards.post_actions_keyboard import *
from config_data.config import load_config, switch_active_channel
from services.database_management import BotDatabase
from config_data.config import get_active_channel

router = Router()

config = load_config()

QUEUE_AUTOPOSTING = False

# =============================== functions =========================================


def get_autoposting():
    return QUEUE_AUTOPOSTING


# ===================================================================================


# ================================= posts main menu =================================

# resend message_copy to my channel
@router.callback_query(F.data == 'publish_post')
async def process_publish_post(callback: CallbackQuery):
    new_message = await callback.message.delete_reply_markup()
    await new_message.send_copy(get_active_channel(), reply_markup=None)
    # возвращаем клавиатуру действий
    await callback.message.edit_reply_markup(reply_markup=create_post_actions_kb())
    await callback.answer()
    
    
# delete message from chat
@router.callback_query(F.data == 'reject_post')
async def process_reject_post(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    
# set edit_post inline buttons markup
@router.callback_query(F.data == 'edit_menu')
async def process_open_edit_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=create_edit_post_kb())

# add post in database (queue)
@router.callback_query(F.data == 'add_to_queue')
async def process_add_to_queue(callback: CallbackQuery):
    db = BotDatabase(config.database.path)
    photo_id = callback.message.photo[0].file_id
    post_text = callback.message.caption
    db.add_post_in_queue(post_text, photo_id)
    await callback.message.edit_reply_markup(reply_markup=create_main_actions_add_to_queue())
    await callback.answer()
    
# get new post
@router.callback_query(F.data == 'swap_post')
async def process_swap_post(callback: CallbackQuery):
    await callback.message.delete()
    await get_active_channel_post(callback.message)
 
    
# ===================================================================================    
    
    
    
    
    
  
# ========================= edit post menu ==========================================   

# delete last paragraph in post
@router.callback_query(F.data == 'delete_last_string')
async def process_delete_last_string(callback: CallbackQuery):
    text = callback.message.caption
    if text:
        split_text = text.split('\n')
        new_text = '\n'.join(split_text[:-1])
        await callback.message.edit_caption(caption=new_text, reply_markup=create_edit_post_kb())
    else:
        await callback.answer()
        

# delete first paragraph in post
@router.callback_query(F.data == 'delete_first_string')
async def process_delete_first_string(callback: CallbackQuery):
    text = callback.message.caption
    if text:
        split_text = text.split('\n')
        new_text = split_text[0] + '\n'.join(split_text[2:])
        await callback.message.edit_caption(caption=new_text, reply_markup=create_edit_post_kb())
    else:
        await callback.answer()
        
       
# add link to my channel in post text
@router.callback_query(F.data == 'add_link')
async def process_add_link_to_my_channel(callback: CallbackQuery):
    new_text = callback.message.caption + f'\n\n{get_active_channel()}'
    try:
        await callback.message.edit_caption(caption=new_text, reply_markup=create_edit_post_kb())
    except TelegramBadRequest:
        print('сообщение получается слишком длинным')
        await callback.answer()
        
# back to main_actions inline keyboard 
@router.callback_query(F.data == 'main_actions')
async def process_back_to_main_actions_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=create_post_actions_kb())
    
# ====================================================================================   
    
    
    


# ============================ bot main menu ============================================



# publick last post in queue
@router.callback_query(F.data == 'last_post')
async def process_public_next_post_in_queue(callback: CallbackQuery):
    db = BotDatabase(config.database.path)
    post = db.get_last()
    if post:
        id, text, image = post
        await callback.message.answer_photo(image, text, reply_markup=create_post_actions_kb())
    await callback.answer()


# publick next post in queue
@router.callback_query(F.data == 'next_post')
async def process_public_next_post_in_queue(callback: CallbackQuery):
    db = BotDatabase(config.database.path)
    post = db.get_next()
    if post:
        id, text, image = post
        await callback.message.answer_photo(image, text, reply_markup=create_post_actions_kb())
    await callback.answer()


# start queue auto-posting 
@router.callback_query(F.data == 'start_stop_queue')
async def process_start_stop_public_queue(callback: CallbackQuery):
    global QUEUE_AUTOPOSTING
    QUEUE_AUTOPOSTING = not QUEUE_AUTOPOSTING
    print('автопостинг очереди', QUEUE_AUTOPOSTING)
    text = format_main_menu_text(QUEUE_AUTOPOSTING)
    if QUEUE_AUTOPOSTING:
        await callback.message.edit_text(text, 
                                        reply_markup=create_main_menu_kb())
        await start_queue()
    else:
        await callback.message.edit_text(text, 
                                        reply_markup=create_main_menu_kb())
        await stop_queue()


# switch active channel
@router.callback_query(F.data.in_(config.tg_channel.channel_names))
async def process_switch_active_channel(callback: CallbackQuery):
    await switch_active_channel(callback.data)
    text = format_main_menu_text(QUEUE_AUTOPOSTING)
    await callback.message.edit_text(text=text,
                                     reply_markup=create_main_menu_kb())
    await callback.answer()


# open bot_mode menu
@router.callback_query(F.data == 'bot_mode')
async def process_open_bot_mode_menu(callback: CallbackQuery):
    await callback.message.edit_text(text='выбери канал для управления',
                                  reply_markup=create_bot_mode_menu())