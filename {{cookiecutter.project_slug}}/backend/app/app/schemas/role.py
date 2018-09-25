# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields

# Import app code
from .base import BaseSchema


class RoleSchema(BaseSchema):
    # Own properties
    id = fields.Int()
    created_at = fields.DateTime()
    name = fields.Str()
    users = fields.Nested(
        "UserSchema",
        only=["id", "first_name", "last_name", "email", "is_active", "is_superuser"],
        many=True,
    )
