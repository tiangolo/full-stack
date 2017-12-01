# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields
# Import app code
from .base import BaseSchema


class TokenSchema(BaseSchema):
    # Own properties
    access_token = fields.Str()
    refresh_token = fields.Str()