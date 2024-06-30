import sqlite3
import asyncio
from config_data.config import load_config

  
class BotDatabase:
    def __init__(self, database_path: str) -> None:
        self.path = database_path
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
    
    def add_post_in_queue(self, post_text, image_url):

        data = (post_text, image_url)
        self.cursor.execute('''
                       INSERT INTO Queue(post_text, image_url)
                       VALUES (?, ?)
                       ''', data)

        self.connection.commit()
    
    def get_queue(self):
        self.cursor.execute('SELECT * FROM Queue')
        return self.cursor.fetchall()
    
    def get_next(self):
        self.cursor.execute('SELECT * FROM Queue LIMIT 1')
        post = self.cursor.fetchone()
        self.cursor.execute('DELETE FROM Queue WHERE id in (SELECT id FROM Queue LIMIT 1)')
        self.connection.commit()
        return post
    
    async def create_database(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_text TEXT NOT NULL,
            image_url TEXT NOT NULL
            )
            ''')
        
        self.connection.commit()
    

    
