# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields

# Import app code
from .base import BaseSchema
from .role import RoleSchema


class UserSchema(BaseSchema):
    # Own properties
    id = fields.Int()
    created_at = fields.DateTime()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    is_active = fields.Bool()
    is_superuser = fields.Bool()
    roles = fields.Nested(RoleSchema, only=("id", "name"), many=True)
