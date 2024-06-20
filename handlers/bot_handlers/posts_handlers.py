from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from keyboards.post_actions_keyboard import create_post_actions_kb 
from config_data.config import load_config

router = Router()

config = load_config()
ADMIN_IDS = config.tg_bot.admin_ids
PARSER_ACCOUNT_ID = config.tg_bot.parser_account_id

# resend parsers-account message with keyboard (переотправка сообщения с клавиатурой откланения или публикации)
@router.message(lambda x: str(x.from_user.id) == PARSER_ACCOUNT_ID)
async def process_resend_post_with_buttons(message: Message):
    for admin in ADMIN_IDS:
        await message.send_copy(admin, reply_markup=create_post_actions_kb())