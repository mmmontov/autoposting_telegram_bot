from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list[str]
    parser_account_id: str
    

@dataclass
class TgAccount:
    api_id: int
    api_hash: str
    phone: str
    
    
@dataclass
class TgChannel:
    channel_names: list[str]
    
    
@dataclass
class Database:
    path: str
    
    
@dataclass
class Config:
    tg_bot: TgBot
    tg_account: TgAccount
    tg_channel: TgChannel
    database: Database
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(env.list('ADMIN_IDS')),
            parser_account_id=env('PARSER_ACCOUNT_ID')
        ),
        tg_account=TgAccount(
            api_id=int(env('API_ID')),
            api_hash=env('API_HASH'),
            phone=env('PHONE')
        ),
        tg_channel=TgChannel(
            channel_names=list(env.list('CHANNEL_IDS'))
        ),
        database=Database(
            path=env('DATABASE_PATH')
        )
    )

config = load_config()
channels = config.tg_channel.channel_names

active_channel = channels[0]

async def switch_active_channel(channel_id: str):
    global active_channel
    active_channel = channel_id
    print(f'активный канал переключен на {active_channel}')

def get_active_channel():
    global active_channel
    return active_channel