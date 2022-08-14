from aiohttp import web

from app.context import AppContext
from .api.v1 import auth, users


def wrap_handler(handler, context):
    async def wrapper(request):
        return await handler(request, context)

    return wrapper


def setup_routes(app: web.Application, ctx: AppContext) -> None:
    app.router.add_post(
        '/v1/auth/signup',
        wrap_handler(
            auth.signup,
            ctx
        )
    )
    app.router.add_post(
        '/v1/auth/login',
        wrap_handler(
            auth.login,
            ctx
        )
    )
    app.router.add_get(
        '/v1/users',
        wrap_handler(
            users.get_users_list,
            ctx
        )
    )
    app.router.add_get(
        r'/v1/users/{user_id:\d+}',
        wrap_handler(
            users.get_users_detail,
            ctx
        )
    )
    app.router.add_put(
        r'/v1/users/{user_id:\d+}',
        wrap_handler(
            users.update_patch_user,
            ctx
        )
    )
    app.router.add_patch(
        r'/v1/users/{user_id:\d+}',
        wrap_handler(
            users.update_patch_user,
            ctx
        )
    )
    app.router.add_delete(
        r'/v1/users/{user_id:\d+}',
        wrap_handler(
            users.update_patch_user,
            ctx
        )
    )
