# -*- coding: utf-8 -*-

# Import standard library packages

# Import installed packages
from marshmallow import fields

# Import app code
from .base import BaseSchema


class ScalarSchema(BaseSchema):
    # Own properties
    value = fields.Float()
