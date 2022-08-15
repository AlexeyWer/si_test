import datetime as dt

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from .db import Role, roles, users


def create_roles_admin(engine: Engine) -> None:
    with engine.connect() as conn:
        admin_role = insert(roles).values(
            title=Role.admin
        ).on_conflict_do_update(
            index_elements=['title'],
            set_=dict(title=Role.admin)
        )
        admin_role_id = conn.execute(admin_role).inserted_primary_key['id']
        blocked_role = insert(roles).values(
            title=Role.blocked
        ).on_conflict_do_update(
            index_elements=['title'],
            set_=dict(title=Role.blocked)
        )
        conn.execute(blocked_role)
        only_read_role = insert(roles).values(
            title=Role.only_read
        ).on_conflict_do_update(
            index_elements=['title'],
            set_=dict(title=Role.only_read)
        )
        conn.execute(only_read_role)
        admin = insert(users).values(
            first_name='admin',
            username='admin',
            password='admin',
            date_birth=dt.datetime.fromisoformat('1970-01-01'),
            role=admin_role_id
        ).on_conflict_do_nothing()
        conn.execute(admin)
