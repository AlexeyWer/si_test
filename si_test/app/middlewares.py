import os
import json
from typing import Callable

from aiohttp import web
import jwt

from . import crud
from .context import AppContext

JWT_SECRET = os.getenv('JWT_SECRET', 'fake_secret')
JWT_ALGORITH = 'HS256'
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24


async def json_response(body: dict = None, **kwargs) -> web.Response:
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)


class AuthMiddleware:

    def __init__(self, context: AppContext):
        self.context = context

    @web.middleware
    async def middleware(self, request: web.Request, handler: Callable):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITH]
                )
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return await json_response(
                    {'message': 'Token is invalid'}, status=400
                )
            user = await crud.get_user_by_id(self.context, payload['user_id'])
            if user is None:
                return await handler(request)
            request.user = user
            return await handler(request)
