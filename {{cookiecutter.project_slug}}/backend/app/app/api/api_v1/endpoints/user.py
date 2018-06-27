# -*- coding: utf-8 -*-

# Import standard library modules

# Import installed modules
# # Import installed packages
from flask import abort
from webargs import fields
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import (get_current_user, jwt_required)

# Import app code
from app.main import app
from app.api.api_v1.api_docs import docs, security_params
from app.core import config
from app.core.security import pwd_context
from app.core.database import db_session
from app.core.celery_app import celery_app

# Import Schemas
from app.schemas.user import UserSchema
# Import models
from app.models.user import User
from app.models.group import Group


@docs.register
@doc(
    description='Retrieve the users that the given user manages from groups',
    security=security_params,
    tags=['users'])
@app.route(f'{config.API_V1_STR}/users/', methods=['GET'])
@marshal_with(UserSchema(many=True))
@jwt_required
def route_users_get():
    current_user = get_current_user()

    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')

    users = [current_user]

    if current_user.is_superuser:
        return db_session.query(User).all()

    elif current_user.groups_admin:
        # return all the users in the groups the user is admin in
        users = []
        for group in current_user.groups_admin:
            users.extend(group.users)

        return users

    # return the current user's data, but in a list
    return users


@docs.register
@doc(
    description='Create new user',
    security=security_params,
    tags=['users'])
@app.route(f'{config.API_V1_STR}/users/', methods=['POST'])
@use_kwargs({
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
    'first_name': fields.Str(),
    'last_name': fields.Str(),
    'group_id': fields.Int(required=True),
})
@marshal_with(UserSchema())
@jwt_required
def route_users_post(email=None,
                     password=None,
                     first_name=None,
                     last_name=None,
                     group_id=None):
    current_user = get_current_user()

    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')
    elif not current_user.is_superuser:
        abort(400, 'Only a superuser can execute this action')

    user = db_session.query(User).filter(User.email == email).first()

    if user:
        return abort(
            400,
            f'The user with this email already exists in the system: {email}')

    group = db_session.query(Group).filter(Group.id == group_id).first()

    if group is None:
        abort(400, f'There is no group with id: "{group_id}"')
    user = User(
        email=email,
        password=pwd_context.hash(password),
        first_name=first_name,
        last_name=last_name,
        group=group)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@docs.register
@doc(
    description='Get current user',
    security=security_params,
    tags=['users'])
@app.route(f'{config.API_V1_STR}/users/me', methods=['GET'])
@marshal_with(UserSchema())
@jwt_required
def route_users_me_get():
    current_user = get_current_user()
    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')
    return current_user


@docs.register
@doc(
    description='Get a specific user by ID',
    security=security_params,
    tags=['users'])
@app.route(f'{config.API_V1_STR}/users/<int:user_id>', methods=['GET'])
@marshal_with(UserSchema())
@jwt_required
def route_users_id_get(user_id):
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')

    user = db_session.query(User).filter(
        User.id == user_id).first()  # type: User

    if not user:
        return abort(400, f'The user with id: {user_id} does not exists')

    if current_user.is_superuser:
        # Return everything, don't abort
        pass
    elif user.group in current_user.groups_admin:
        # Return everything, don't abort
        pass

    else:
        abort(400, 'Not authorized')

    return user
