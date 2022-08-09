from aiohttp import web

from app.context import AppContext


def wrap_handler(handler, context):
    async def wrapper(request):
        return await handler(request, context)

    return wrapper


def setup_routes(app: web.Application, ctx: AppContext) -> None:
    app.router.add_get(
        '/v1/',
        wrap_handler(
            'My handle', # TODO
            ctx,
        ),
    )
    app.router.add_get(
        '/v1/',
        wrap_handler(
            'My handle', # TODO
            ctx,
        ),
    )
