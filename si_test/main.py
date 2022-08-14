import asyncio
import argparse

from aiohttp import web
from sqlalchemy import create_engine

from app.context import AppContext
from app.middlewares import AuthMiddleware
from app import routes
from app.db import metadata
from app.init_db import create_roles_admin


async def create_app(args):
    app = web.Application()

    ctx = AppContext(secrets_dir=args.secrets_dir)

    auth_middleware = AuthMiddleware(ctx)
    app.middlewares.append(auth_middleware.middleware)

    engine = create_engine(ctx.secrets.get('postgres_dsn'))
    metadata.create_all(engine)
    create_roles_admin(engine)

    app.on_startup.append(ctx.on_startup)
    app.on_shutdown.append(ctx.on_shutdown)

    routes.setup_routes(app, ctx)

    return app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--secrets-dir', type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    app = asyncio.get_event_loop().run_until_complete(create_app(args))

    web.run_app(app)


if __name__ == '__main__':
    main()
