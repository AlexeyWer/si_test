from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


BIRTH_DATE_FORMAT = '%d-%m-%Y'


class User:
    def __init__(self,
                 username: str,
                 id: int = None,
                 first_name: str = None,
                 last_name: str = None,
                 date_birth: datetime = None,
                 role: str = None,
                 created: datetime = None,
                 *args, **kwargs):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.date_birth = date_birth
        self.role = role
        self.created = created

    def __repr__(self):
        if self.id:
            return f'<User(id={self.id}, username={self.username})>'
        return f'<User(username={self.username})>'


class ResponseUserSchema(Schema):
    id = fields.Int(validate=Range(min=0), required=False)
    username = fields.Str(validate=Length(min=1, max=256), required=True)


class UpdateUserSchema(ResponseUserSchema):
    first_name = fields.Str(validate=Length(min=1, max=256), required=True)
    last_name = fields.Str(validate=Length(min=1, max=256), required=True)
    date_birth = fields.Date(format=BIRTH_DATE_FORMAT, required=True)


class AuthUserSchema(Schema):
    password = fields.Str(validate=Length(min=1, max=256), required=True)
    username = fields.Str(validate=Length(min=1, max=256), required=True)
