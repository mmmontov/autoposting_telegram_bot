from pyrogram import Client, filters
from pyrogram.types import Message


class ChannelsParser:
    doner_channels = [
        'doner_channel_1',
    ]
    
    
    async def channels_parser(client: Client, message: Message):
        await message.forward('autopost_mishabot')
    
print('handlers on')    
