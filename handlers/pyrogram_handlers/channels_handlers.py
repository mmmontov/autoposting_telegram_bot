from pyrogram import Client, filters
from pyrogram.types import Message


class ChannelsParser:
    doner_channels = [
        'mash',
        'doner_channel_1',
        'moscowach',
        'rozetked',
        'whackdoor',
        'codecamp',
        'Cbpub',
        'Wylsared',
        'exploitex',
        'Wylsared',
        'trends',
        'biggeekru',
        'Romancev768',      
        'misha_testchannel'                             
    ]
    
# doner_channels = [
#     'https://t.me/retsepty5',
#     'https://t.me/Wylsared',
#     'https://t.me/mash',
#     'https://t.me/moscowach',
#     'https://t.me/Cbpub',
#     'https://t.me/exploitex',
#     'https://t.me/nemorgenshtern',
#     'https://t.me/streaminside',
#     'https://t.me/trends',
#     'https://t.me/Romancev768',
#     'https://t.me/whackdoor',
#     'https://t.me/biggeekru',
#     'https://t.me/rozetked',
#     'https://t.me/codecamp',
# ]
    
    async def channels_parser(client: Client, message: Message):
        print(f'поймано')
        await message.forward('autopost_mishabot')
    
# print('handlers on')    
