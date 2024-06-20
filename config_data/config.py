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
class Config:
    tg_bot: TgBot
    tg_account: TgAccount
    
    
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
        )
    )
