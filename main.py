import asyncio, schedule
from aiogram import Bot, Dispatcher
from handlers.bot_handlers import user_handlers, posts_handlers, callback_handlers, admins_handlers
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler

from keyboards.main_menu import set_main_menu
from handlers.pyrogram_handlers.channels_handlers import ChannelsParser 
from config_data.config import load_config
from services.database_management import BotDatabase

config = load_config()
BOT_TOKEN = config.tg_bot.token

API_ID = config.tg_account.api_id
API_HASH = config.tg_account.api_hash
PHONE = config.tg_account.phone


async def main():
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    # парсинг тг каналов временно отключен
    # client: Client = Client('my_client', api_id=API_ID, api_hash=API_HASH, phone_number=PHONE)
    # client.add_handler(MessageHandler(ChannelsParser.channels_parser, filters=filters.chat(ChannelsParser.doner_channels)))

    dp.include_router(admins_handlers.router)
    dp.include_router(user_handlers.router)   
    # dp.include_router(posts_handlers.router) # проект "ворюга" временно закрыт
    dp.include_router(callback_handlers.router)

    await set_main_menu(bot)
    
    # создаём бд если ее нет
    database = BotDatabase(config.database.path)
    await database.create_database()
    
    # await client.start()

    await bot.delete_webhook(drop_pending_updates=True)
    print('бот запустился')
    await dp.start_polling(bot)
    
    # await idle()
    # await client.stop()
    
    
if __name__ == '__main__':
    asyncio.run(main())
    
    