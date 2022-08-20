import logging
from http import HTTPStatus

from aiohttp import web

from app import crud
from app.context import AppContext
from app.db import Role
from app.middlewares import json_response
from app.schema import UpdateUserSchema


log = logging.getLogger(__name__)


class UsersView(web.View):

    def __init__(self, request: web.Request, ctx: AppContext) -> None:
        self.context = ctx
        super().__init__(request)

    async def get(self) -> web.Response:
        user_id = int(self.request.match_info['user_id'])
        user = await crud.get_user_by_id(self.context, user_id)
        if user is None:
            return await json_response(
                {'errors': f'User with id={user_id} not found'},
                status=HTTPStatus.BAD_REQUEST
            )
        return await json_response(
            {'result': user.to_response()}, status=HTTPStatus.OK
        )



async def get_users_detail(request: web.Request,
                           context: AppContext) -> web.Response:
    user_id = int(request.match_info['user_id'])
    user = await crud.get_user_by_id(context, user_id)
    if user is None:
        return await json_response(
            {'errors': f'User with id={user_id} not found'},
            status=HTTPStatus.BAD_REQUEST
        )
    return await json_response(
        {'result': user.to_response()}, status=HTTPStatus.OK
    )


async def get_users_list(request: web.Request,
                         context: AppContext) -> web.Response:
    users = await crud.get_all_users(context)
    return await json_response({'result': users}, status=HTTPStatus.OK)


async def update_patch_user(request: web.Request,
                            context: AppContext) -> web.Response:
    if request.user is None or not request.user.role == Role.admin:
        return await json_response(
            {'errors': 'The method is not available to you'},
            status=HTTPStatus.FORBIDDEN
        )
    user_id = int(request.match_info['user_id'])
    user_data = await request.json()
    if request.method == 'PUT':
        schema = UpdateUserSchema()
    elif request.method == 'PATCH':
        schema = UpdateUserSchema(partial=True)
    data = schema.load(user_data)
    update_user = await crud.update_patch_user_by_id(context, user_id, data)
    return await json_response(
        {'result': update_user.to_response()}, status=HTTPStatus.OK
    )


async def delete_user(request: web.Request,
                      context: AppContext) -> web.Response:
    if request.user is None or not request.user.role == Role.admin:
        return await json_response(
            {'errors': 'The method is not available to you'},
            status=HTTPStatus.FORBIDDEN
        )
    user_id = int(request.match_info['user_id'])
    user = await crud.get_user_by_id(context, user_id)
    if not user:
        return await json_response(
            {'errors': f'User with id={user_id} not found'},
            status=HTTPStatus.BAD_REQUEST
        )
    await crud.delete_user_by_id(context, user_id)
    return await json_response(status=HTTPStatus.NO_CONTENT)
