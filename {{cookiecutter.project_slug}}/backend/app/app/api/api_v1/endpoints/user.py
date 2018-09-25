# -*- coding: utf-8 -*-

# Import standard library modules

# Import installed modules
# # Import installed packages
from flask import abort
from webargs import fields
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import get_current_user, jwt_required

# Import app code
from app.api.api_v1.api_docs import docs, security_params
from app.core import config
from app.core.security import pwd_context
from app.db.flask_session import db_session
from app.core.celery_app import celery_app
from app.db.utils import check_if_user_is_active, check_if_user_is_superuser, get_users, get_user_by_username, create_user, get_user_by_id, get_role_by_id, assign_role_to_user

from app.main import app

# Import Schemas
from app.schemas.user import UserSchema

# Import models
from app.models.user import User
from app.models.role import Role


@docs.register
@doc(
    description="Retrieve the users",
    security=security_params,
    tags=["users"],
)
@app.route(f"{config.API_V1_STR}/users/", methods=["GET"])
@marshal_with(UserSchema(many=True))
@jwt_required
def route_users_get():
    current_user = get_current_user()

    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")
    if check_if_user_is_superuser(current_user):
        return get_users(db_session)
    else:
        # return the current user's data, but in a list
        return [current_user]


@docs.register
@doc(description="Create new user", security=security_params, tags=["users"])
@app.route(f"{config.API_V1_STR}/users/", methods=["POST"])
@use_kwargs(
    {
        "email": fields.Str(required=True),
        "password": fields.Str(required=True),
        "first_name": fields.Str(),
        "last_name": fields.Str(),
    }
)
@marshal_with(UserSchema())
@jwt_required
def route_users_post(
    email=None, password=None, first_name=None, last_name=None,
):
    current_user = get_current_user()

    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")
    elif not check_if_user_is_superuser(current_user):
        abort(400, "Only a superuser can execute this action")

    user = get_user_by_username(email, db_session)

    if user:
        return abort(
            400, f"The user with this email already exists in the system: {email}"
        )
    user = create_user(db_session, email, password, first_name, last_name )
    return user

@docs.register
@doc(description="Create new user without the need to be logged in", tags=["users"])
@app.route(f"{config.API_V1_STR}/users/open", methods=["POST"])
@use_kwargs(
    {
        "email": fields.Str(required=True),
        "password": fields.Str(required=True),
        "first_name": fields.Str(),
        "last_name": fields.Str(),
    }
)
@marshal_with(UserSchema())
def route_users_post_open(
    email=None, password=None, first_name=None, last_name=None,
):
    if not config.USERS_OPEN_REGISTRATION:
        abort(403, "Open user resgistration is forbidden on this server")
    
    user = get_user_by_username(email, db_session)

    if user:
        return abort(
            400, f"The user with this email already exists in the system: {email}"
        )

    user = create_user(db_session, email, password, first_name, last_name)
    return user


@docs.register
@doc(description="Get current user", security=security_params, tags=["users"])
@app.route(f"{config.API_V1_STR}/users/me", methods=["GET"])
@marshal_with(UserSchema())
@jwt_required
def route_users_me_get():
    current_user = get_current_user()
    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")
    return current_user


@docs.register
@doc(description="Get a specific user by ID", security=security_params, tags=["users"])
@app.route(f"{config.API_V1_STR}/users/<int:user_id>", methods=["GET"])
@marshal_with(UserSchema())
@jwt_required
def route_users_id_get(user_id):
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")

    user = get_user_by_id(user_id, db_session)

    if not user:
        return abort(400, f"The user with id: {user_id} does not exists")

    if not check_if_user_is_superuser(current_user):
        return abort(400, "Not authorized")
    return user


@docs.register
@doc(description="Assign a role to a user by ID", security=security_params, tags=["users"])
@app.route(f"{config.API_V1_STR}/users/<int:user_id>/roles/", methods=["POST"])
@use_kwargs({
    "role_id": fields.Int(required=True),
})
@marshal_with(UserSchema())
@jwt_required
def route_users_assign_role_post(user_id, role_id):
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, "Could not authenticate user with provided token")
    elif not check_if_user_is_active(current_user):
        abort(400, "Inactive user")
    elif not check_if_user_is_superuser(current_user):
        abort(404, "Not authorized")

    user = get_user_by_id(user_id, db_session)
    if not user:
        return abort(400, f"The user with id: {user_id} does not exists")
    
    role = get_role_by_id(role_id, db_session)
    if not role:
        return abort(400, f"The role does not exist")
    
    updated_user = assign_role_to_user(role, user, db_session)
    return updated_user
