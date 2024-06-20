import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove

router = Router()

# resend message_copy to my channel
@router.callback_query(F.data == 'publish_post')
async def process_publish_post(callback: CallbackQuery):
    my_channel: str = '@misha_testchannel'
    new_message = await callback.message.delete_reply_markup()
    await new_message.send_copy(my_channel, reply_markup=None)
    await callback.answer()
    
    
# delete message from chat
@router.callback_query(F.data == 'reject_post')
async def process_reject_post(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()