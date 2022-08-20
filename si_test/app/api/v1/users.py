import logging
from http import HTTPStatus

from aiohttp import web

from app import crud
from app.db import Role
from app.middlewares import json_response
from app.schema import UpdateUserSchema


log = logging.getLogger(__name__)


class UsersView(web.View):
    URL_PATH = r'users/{user_id:\d+}/'

    @property
    def user_id(self):
        return int(self.request.match_info['user_id'])

    @property
    def context(self):
        return self.request.app['context']

    async def check_permissions(self) -> None:
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return
        if (self.request.user is None
           or not self.request.user.role == Role.admin):
            raise web.HTTPForbidden(
                reason=f'{self.request.method} method is not available to you'
            )

    async def get(self) -> web.Response:
        await self.check_permissions()
        user = await crud.get_user_by_id(self.context, self.user_id)
        if user is None:
            return await json_response(
                {'errors': f'User with id={self.user_id} not found'},
                status=HTTPStatus.BAD_REQUEST
            )
        return await json_response(
            {'result': user.to_response()}, status=HTTPStatus.OK
        )

    async def put(self) -> web.Response:
        await self.check_permissions()
        user_data = await self.request.json()
        schema = UpdateUserSchema()
        data = schema.load(user_data)
        update_user = await crud.update_patch_user_by_id(
            self.context, self.user_id, data
        )
        return await json_response(
            {'result': update_user.to_response()}, status=HTTPStatus.OK
        )

    async def patch(self) -> web.Response:
        await self.check_permissions()
        user_data = await self.request.json()
        schema = UpdateUserSchema(partial=True)
        data = schema.load(user_data)
        update_user = await crud.update_patch_user_by_id(
            self.context, self.user_id, data
        )
        return await json_response(
            {'result': update_user.to_response()}, status=HTTPStatus.OK
        )

    async def delete(self):
        await self.check_permissions()
        user = await crud.get_user_by_id(self.context, self.user_id)
        if not user:
            return await json_response(
                {'errors': f'User with id={self.user_id} not found'},
                status=HTTPStatus.BAD_REQUEST
            )
        await crud.delete_user_by_id(self.context, self.user_id)
        return await json_response(status=HTTPStatus.NO_CONTENT)


async def get_users_list(request: web.Request) -> web.Response:
    context = request.app['context']
    users = await crud.get_all_users(context)
    return await json_response({'result': users}, status=HTTPStatus.OK)
