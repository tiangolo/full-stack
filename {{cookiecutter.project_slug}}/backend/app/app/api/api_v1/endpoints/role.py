# -*- coding: utf-8 -*-

# Import standard library modules

# Import installed modules
# # Import installed packages
from flask import abort
from webargs import fields
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import get_current_user, jwt_required

# Import app code
from app.main import app
from app.api.api_v1.api_docs import docs, security_params
from app.core import config
from app.db.flask_session import db_session
from app.core.celery_app import celery_app
from app.db.utils import (check_if_user_is_active, check_if_user_is_superuser, get_role_by_name, create_role, get_roles, get_user_roles)

# Import Schemas
from app.schemas.role import RoleSchema
from app.schemas.msg import MsgSchema

# Import models
from app.models.role import Role
from app.models.user import User


@docs.register
@doc(description="Create a new role", security=security_params, tags=["roles"])
@app.route(f"{config.API_V1_STR}/roles/", methods=["POST"])
@use_kwargs({"name": fields.Str(required=True)})
@marshal_with(RoleSchema())
@jwt_required
def route_roles_post(name=None):
    current_user = get_current_user()
    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")
    elif not check_if_user_is_superuser(current_user):
        abort(400, "Not a superuser")

    role = get_role_by_name(name, db_session)
    if role:
        return abort(400, f"The role: {name} already exists in the system")
    role = create_role(name, db_session)
    return role


@docs.register
@doc(
    description="Retrieve the roles of the user",
    security=security_params,
    tags=["roles"],
)
@app.route(f"{config.API_V1_STR}/roles/", methods=["GET"])
@marshal_with(RoleSchema(only=("id", "name", "created_at", "name"), many=True))
@jwt_required
def route_roles_get():
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")

    if check_if_user_is_superuser(current_user):
        return get_roles(db_session)
    else:
        return get_user_roles(current_user)
