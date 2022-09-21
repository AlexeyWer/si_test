from aiohttp import web

from .api.v1 import auth, users


def setup_routes(app: web.Application) -> None:
    prefix = '/v1/'
    app.router.add_post(
        prefix + 'auth/signup/',
        auth.signup
    )
    app.router.add_post(
        prefix + 'auth/login/',
        auth.login
    )
    app.router.add_get(
        prefix + users.UsersView.URL_PATH_LIST,
        users.UsersView.get_users_list,
    )
    app.router.add_view(
        prefix + users.UsersView.URL_PATH_DETAIL,
        users.UsersView
    )
