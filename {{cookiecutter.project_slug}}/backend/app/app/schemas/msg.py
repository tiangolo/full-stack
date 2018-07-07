# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields

# Import app code
from .base import BaseSchema


class MsgSchema(BaseSchema):
    # Own properties
    msg = fields.Str()
