import os
import typing as tp

from databases import Database


class AppContext:
    def __init__(self, *, secrets_dir: str):
        self.db: tp.Optional[Database] = None

    async def on_startup(self, app=None):
        self.db = Database(os.getenv('DATABASE_URL'))
        await self.db.connect()

    async def on_shutdown(self, app=None):
        await self.db.disconnect()
