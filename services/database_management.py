import sqlite3
import asyncio
from config_data.config import load_config
from config_data.config import get_active_channel

config = load_config()

  
class BotDatabase:
    def __init__(self, database_path: str) -> None:
        self.path = database_path
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
    
    def add_post_in_queue(self, post_text, image_url):
        channel_name = self.format_id_to_queue(get_active_channel())
        data = (post_text, image_url)
        self.cursor.execute(f'''
                       INSERT INTO {channel_name}(post_text, image_url)
                       VALUES (?, ?)
                       ''', data)

        self.connection.commit()
    
    def get_queue(self):
        channel_name = self.format_id_to_queue(get_active_channel())
        self.cursor.execute(f'SELECT * FROM {channel_name}')
        return self.cursor.fetchall()
    
    def get_next(self, channel=None):
        channel_name = self.format_id_to_queue(get_active_channel())
        if channel:
            channel_name = self.format_id_to_queue(channel)
        
        self.cursor.execute(f'SELECT * FROM {channel_name} LIMIT 1')
        post = self.cursor.fetchone()
        
        self.cursor.execute(f'DELETE FROM {channel_name} WHERE id in (SELECT id FROM {channel_name} LIMIT 1)')
        self.connection.commit()
        return post
    
    def get_last(self):
        channel_name = self.format_id_to_queue(get_active_channel())
        self.cursor.execute(f'SELECT * FROM {channel_name} ORDER BY id DESC LIMIT 1')
        post = self.cursor.fetchone()
        
        self.cursor.execute(f'DELETE FROM {channel_name} WHERE id in (SELECT id FROM {channel_name} ORDER BY id DESC LIMIT 1)')
        self.connection.commit()
        return post
    
    async def create_database(self):
        for bot in config.tg_channel.channel_names:
            channel_name = self.format_id_to_queue(bot)
            self.cursor.execute(
                f'''
                CREATE TABLE IF NOT EXISTS {channel_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_text TEXT NOT NULL,
                image_url TEXT NOT NULL
                )
                ''')
        
        self.connection.commit()
    
    @staticmethod
    def format_id_to_queue(id: str):
        return f'{id[1:]}_queue'
        
    

    
