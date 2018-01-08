# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields
# Import app code
from .base import BaseSchema
from .group import GroupSchema


class UserSchema(BaseSchema):
    # Own properties
    id = fields.Int()
    created_at = fields.DateTime()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    is_active = fields.Bool()
    is_superuser = fields.Bool()
    group = fields.Nested(GroupSchema, only=('id', 'name'))
    groups_admin = fields.Nested(
        GroupSchema, only=('id', 'name'), many=True)
