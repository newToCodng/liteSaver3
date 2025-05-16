import os
import asyncpg
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/always/liteSaverBackend/.env")
print("ENV:", os.environ.get("DATABASE_URL"))


class Database:
    def __init__(self):
        self.db_pool = None
        self.database_url = os.environ["DATABASE_URL"]

    async def connect(self):
        self.db_pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        if self.db_pool:
            await self.db_pool.close()
            self.db_pool = None

    def get_pool(self):
        return self.db_pool


db = Database()
