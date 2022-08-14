from enum import Enum, unique

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    MetaData,
    String,
    Table,
    Enum as PgEnum
)
from sqlalchemy.sql import func


@unique
class Role(str, Enum):
    admin = 'admin'
    blocked = 'blocked'
    only_read = 'only_read'


metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(128),  nullable=True),
    Column('last_name', String(128),  nullable=True),
    Column('username', String(128), unique=True),
    Column('password', String(128), nullable=False),
    Column('date_birth', DateTime, nullable=True),
    Column('role', Integer, ForeignKey('roles.id')),
    Column('created', DateTime(timezone=True), server_default=func.now()),
)

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'title',
        PgEnum(Role, name='role'),
        unique=True,
    ),
)
