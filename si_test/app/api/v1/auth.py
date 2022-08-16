import logging
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from aiohttp import web
from app import crud
from app.context import AppContext
from app.middlewares import (JWT_ALGORITH, JWT_EXP_DELTA_SECONDS, JWT_SECRET,
                             json_response)
from app.schema import AuthUserSchema
from marshmallow import ValidationError


log = logging.getLogger(__name__)


async def signup(request: web.Request, context: AppContext) -> web.Response:
    user_data = await request.json()
    schema = AuthUserSchema()

    try:
        data = schema.load(user_data)
    except ValidationError as err:
        return await json_response(
            {'errors': err.messages}, status=HTTPStatus.BAD_REQUEST
        )

    try:
        new_user = await crud.create_user(context, data)
    except Exception as err:
        log.error(f'Non handle error: {str(err)}')
        return await json_response(
            {'errors': 'Try again later'},
            status=HTTPStatus.SERVICE_UNAVAILABLE
        )

    message = (f'The user {new_user.username} '
               f'has been successfully registered')
    return await json_response({'message': message}, status=HTTPStatus.CREATED)


async def login(request: web.Request, context: AppContext) -> web.Response:
    user_data = await request.json()
    schema = AuthUserSchema()

    try:
        data = schema.load(user_data)
    except ValidationError as err:
        return await json_response(
            {'errors': err.messages}, status=HTTPStatus.BAD_REQUEST
        )

    try:
        user = await crud.get_user_by_username_password(context, data)
    except Exception as err:
        log.error(f'Non handle error: {str(err)}')
        return await json_response(
            {'errors': 'Try again later'},
            status=HTTPStatus.SERVICE_UNAVAILABLE
        )

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
