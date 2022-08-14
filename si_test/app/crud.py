from typing import List

from sqlalchemy import select, cast, String, update, delete

from .db import users, roles, Role
from .schema import User, AuthUserSchema, ResponseUserSchema, UpdateUserSchema
from .context import AppContext


async def create_user(context: AppContext, user: AuthUserSchema) -> User:
    default_role_id_query = select(
        roles
        ).where(
            roles.c.title == Role.only_read
        )
    default_role_id = await context.db.execute(default_role_id_query)
    query = users.insert().values(
        username=user['username'],
        password=user['password'],
        role=default_role_id
    )
    id_new_user = await context.db.execute(query=query)
    return User(**user, id=id_new_user)


async def get_user_by_username_password(context: AppContext,
                                        login_user: AuthUserSchema) -> User:
    query = users.select().where(
        users.c.username == login_user['username'],
        users.c.password == login_user['password'],
    )
    exists = await context.db.fetch_one(query.as_scalar())
    if not exists:
        return False
    row = await context.db.fetch_one(query)
    return User(**row)


async def get_user_by_id(context: AppContext, user_id: int) -> User:
    query = select(
        users.c.id,
        users.c.username,
        users.c.first_name,
        users.c.last_name,
        cast(roles.c.title.label('role'), String)
    ).where(
        users.c.id == user_id,
    ).select_from(
        users
    ).join(
        roles, users.c.role == roles.c.id
    )
    exists = await context.db.fetch_one(query.as_scalar())
    if not exists:
        return False
    row = await context.db.fetch_one(query)
    return User(**row)


async def get_all_users(context: AppContext) -> List[dict]:
    query = select(users.c.id, users.c.username).select_from(users)
    rows = await context.db.fetch_all(query)
    return ResponseUserSchema(many=True).dump(rows)


async def update_patch_user_by_id(
        context: AppContext,
        user_id: int,
        update_data: UpdateUserSchema) -> UpdateUserSchema:
    query = update(
        users
    ).where(
        users.c.id == user_id
    ).values(
        **update_data
    )
    await context.db.execute(query=query)
    return update_data


async def delete_user_by_id(context: AppContext,
                            user_id: int) -> None:
    query = delete(
        users
    ).where(
        users.c.id == user_id
    )
    await context.db.execute(query=query)
