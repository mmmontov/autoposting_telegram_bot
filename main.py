import asyncio
from aiogram import Bot, Dispatcher
from handlers.bot_handlers import user_handlers, posts_handlers, callback_handlers
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler

from handlers.pyrogram_handlers.channels_handlers import ChannelsParser 
from config_data.config import load_config

config = load_config()
BOT_TOKEN = config.tg_bot.token

API_ID = config.tg_account.api_id
API_HASH = config.tg_account.api_hash
PHONE = config.tg_account.phone


async def main():
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    client: Client = Client('my_client', api_id=API_ID, api_hash=API_HASH, phone_number=PHONE)
    
    
    client.add_handler(MessageHandler(ChannelsParser.channels_parser, filters=filters.chat(ChannelsParser.doner_channels)))

    dp.include_router(user_handlers.router)   
    dp.include_router(posts_handlers.router)
    dp.include_router(callback_handlers.router)
     
    await client.start()
    await dp.start_polling(bot)
    await idle()
    await client.stop()
    
    
if __name__ == '__main__':
    asyncio.run(main())
    
    