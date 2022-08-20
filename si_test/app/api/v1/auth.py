import logging
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from aiohttp import web
from app import crud
from app.middlewares import (JWT_ALGORITH, JWT_EXP_DELTA_SECONDS, JWT_SECRET,
                             json_response)
from app.schema import AuthUserSchema


log = logging.getLogger(__name__)


async def signup(request: web.Request) -> web.Response:
    context = request.app['context']
    user_data = await request.json()
    schema = AuthUserSchema()
    data = schema.load(user_data)
    new_user = await crud.create_user(context, data)
    message = (f'The user {new_user.username} '
               f'has been successfully registered')
    return await json_response({'message': message}, status=HTTPStatus.CREATED)


async def login(request: web.Request) -> web.Response:
    context = request.app['context']
    user_data = await request.json()
    schema = AuthUserSchema()
    data = schema.load(user_data)
    user = await crud.get_user_by_username_password(context, data)
    if user is None:
        return await json_response(
            {'errors': 'incorrect login or password'},
            status=HTTPStatus.BAD_REQUEST
        )
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITH)
    return await json_response({'token': jwt_token})
