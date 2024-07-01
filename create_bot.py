from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config_data.config import load_config

config = load_config()

bot = Bot(config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))