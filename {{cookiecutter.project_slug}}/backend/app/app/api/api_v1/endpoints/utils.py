# -*- coding: utf-8 -*-

# Import installed modules
# Import installed packages
from webargs import fields
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import jwt_required

# Import app code
from app.main import app
from app.api.api_v1.api_docs import docs, security_params
from app.core import config
from app.core.celery_app import celery_app

# Import Schemas
from app.schemas.msg import MsgSchema

# Import models


@docs.register
@doc(description="Test Celery worker", security=security_params, tags=["utils"])
@app.route(f"{config.API_V1_STR}/test-celery/", methods=["POST"])
@use_kwargs({"word": fields.String(required=True)})
@marshal_with(MsgSchema())
@jwt_required
def route_test_celery(word):
    celery_app.send_task("app.worker.test_celery", args=[word])
    return ({"msg": "Word received"}, 201)
