import typing as tp

from databases import Database

from app.utils import secrets


class AppContext:
    def __init__(self, *, secrets_dir: str):
        self.secrets: secrets.SecretsReader = secrets.SecretsReader(
            secrets_dir
        )
        self.db: tp.Optional[Database] = None

    async def on_startup(self, app=None):
        self.db = await Database(self.secrets.get('postgres_dsn')).connect()

    async def on_shutdown(self, app=None):
        if self.db:
            await self.db.disconnect()