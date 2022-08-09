import datetime as dt

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    MetaData,
    String,
    Table,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


ROLES = {
    'Admin': 'admin',
    'Blocked': 'blocked',
    'Only_read': 'only_read',
}

metadata = MetaData()

users = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(128),),
    Column('last_name', String(128)),
    Column('username', String(128), unique=True),
    Column('password', String(128)),
    Column('date_birth', DateTime, nullable=False),
    Column('role', Integer, ForeignKey('role.id'))
)

roles = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(128), unique=True),
)

def create_roles_admin(engine: Engine) -> None:
    with Session(engine) as session: 
        admin = users(
            first_name='admin',
            username='admin',
            password='admin',
            date_birth=dt.datetime.fromisoformat('1970-01-01'),
            role=roles(title=ROLES['Admin'])   
        )
        blocked_role = roles(title=ROLES['Blocked'])
        only_read_role = roles(title=ROLES['Only_read'])
        session.add_all([admin, blocked_role, only_read_role])


