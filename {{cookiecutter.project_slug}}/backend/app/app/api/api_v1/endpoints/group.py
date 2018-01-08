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
from app.core.database import db_session
from app.core.celery_app import celery_app
# Import Schemas
from app.schemas.group import GroupSchema
from app.schemas.msg import MsgSchema
# Import models
from app.models.group import Group
from app.models.user import User


@docs.register
@doc(
    description='Create a new group',
    security=security_params,
    tags=['groups'])
@app.route(f'{config.API_V1_STR}/groups/', methods=['POST'])
@use_kwargs({
    'name': fields.Str(required=True),
})
@marshal_with(GroupSchema())
@jwt_required
def route_groups_post(name=None):
    current_user = get_current_user()
    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')
    elif not current_user.is_superuser:
        abort(400, 'Not a superuser')

    group = db_session.query(Group).filter(Group.name == name).first()
    if group:
        return abort(400, f'The group: {name} already exists in the system')
    group = Group(name=name)
    db_session.add(group)
    db_session.commit()
    return group


@docs.register
@doc(
    description='Retrieve the groups of the user',
    security=security_params,
    tags=['groups'])
@app.route(f'{config.API_V1_STR}/groups/', methods=['GET'])
@marshal_with(
    GroupSchema(only=('id', 'name', 'created_at', 'name'), many=True))
@jwt_required
def route_groups_get():
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')

    if current_user.is_superuser:
        return db_session.query(Group).all()
    elif current_user.groups_admin:
        return [group for group in current_user.groups_admin]
    else:
        return [current_user.group]


@docs.register
@doc(
    description='Assign user as group Admin',
    security=security_params,
    tags=[
        'groups',
    ])
@app.route(
    f'{config.API_V1_STR}/groups/<int:group_id>/admin_users/',
    methods=['POST'])
@use_kwargs({'user_id': fields.Int(required=True)})
@marshal_with(MsgSchema())
@jwt_required
def route_admin_users_groups_post(group_id=None, user_id=None):
    current_user = get_current_user()  # type: User

    if not current_user:
        abort(400, 'Could not authenticate user with provided token')
    elif not current_user.is_active:
        abort(400, 'Inactive user')

    group = db_session.query(Group).filter_by(
        id=group_id).first()  # type: Group
    user = db_session.query(User).filter(
        User.id == user_id).first()  # type: User

    if not group:
        return abort(400, f'The group with id: {group_id} does not exists')

    if not user:
        return abort(400, f'The user with id: {user_id} does not exists')

    if current_user.is_superuser:
        group.users_admin.append(user)
        db_session.commit()

    else:
        abort(400, 'Not authorized')

    return {
        'msg':
        f'The user with id {user_id} was sucessfully added as an admin of the group with id {group_id}'
    }
