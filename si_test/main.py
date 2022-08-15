import logging
import asyncio
import os

from aiohttp import web
from sqlalchemy import create_engine

from app.context import AppContext
from app.middlewares import AuthMiddleware
from app import routes
from app.db import metadata
from app.init_db import create_roles_admin


log = logging.getLogger(__name__)


async def create_app():
    app = web.Application()

    ctx = AppContext()

    auth_middleware = AuthMiddleware(ctx)
    app.middlewares.append(auth_middleware.middleware)

    engine = create_engine(os.getenv('DATABASE_URL'))
    metadata.create_all(engine)
    create_roles_admin(engine)

    app.on_startup.append(ctx.on_startup)
    app.on_shutdown.append(ctx.on_shutdown)

    routes.setup_routes(app, ctx)

    return app


def main():
    app = asyncio.get_event_loop().run_until_complete(create_app())

    web.run_app(app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
