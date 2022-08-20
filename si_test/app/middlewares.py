import json
import logging
import os
from http import HTTPStatus
from typing import Callable

import jwt
from aiohttp import web
from marshmallow import ValidationError
from aiohttp.web_exceptions import HTTPException

from . import crud
from .context import AppContext


log = logging.getLogger(__name__)

JWT_SECRET = os.getenv('JWT_SECRET', 'fake_secret')
JWT_ALGORITH = 'HS256'
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24


async def json_response(body: dict = None, **kwargs) -> web.Response:
    if not body and 'body' not in kwargs.keys():
        kwargs['body'] = None
        return web.Response(**kwargs)
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
                    {'message': 'Token is invalid'},
                    status=HTTPStatus.BAD_REQUEST
                )
            except Exception as err:
                logging.error(f'Non handle error: {str(err)}')
                return await json_response(
                    {'errors': 'Try again later'},
                    status=HTTPStatus.SERVICE_UNAVAILABLE
                )
            user = await crud.get_user_by_id(self.context, payload['user_id'])
            request.user = user
        return await handler(request)


class ExceptionMiddleware:

    @web.middleware
    async def middleware(self, request: web.Request, handler: Callable):
        try:
            return await handler(request)
        except ValidationError as err:
            return await json_response(
                {'errors': err.messages}, status=HTTPStatus.BAD_REQUEST
            )
        except HTTPException as err:
            return await json_response(
                {'errors': err.text}, status=err.status
            )
        except Exception as err:
            log.error(f'Non handle error: {str(err)}')
            return await json_response(
                {'errors': 'Try again later'},
                status=HTTPStatus.SERVICE_UNAVAILABLE
            )
