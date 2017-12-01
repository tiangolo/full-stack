# Import installed modules
from flask import abort
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import (create_access_token, get_current_user,
                                jwt_required, create_refresh_token,
                                jwt_refresh_token_required)
from webargs import fields

# Import app code
from app.main import app
from ..api_docs import docs, authorization_headers
from app.core import config
from app.core.security import pwd_context
from app.core.database import db_session
# Import Schemas
from app.schemas.token import TokenSchema
from app.schemas.user import UserSchema
# Import models
from app.models.user import User


@docs.register
@doc(
    description='Login user, get an access token for future requests',
    tags=['login'])
@app.route(f'{config.API_V1_STR}/login/', methods=['POST'])
@use_kwargs({
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
})
@marshal_with(TokenSchema())
def route_login(email=None, password=None):
    user = db_session.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        abort(400, 'Incorrect email or password')
    elif not user.active:
        abort(400, 'Inactive user')
    return {
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id)
    }


@docs.register
@doc(description='Refresh access token', tags=['login'])
@app.route(f'{config.API_V1_STR}/login/refresh-token', methods=['POST'])
@use_kwargs(
    {
        'Authorization':
        fields.Str(
            required=True,
            description=
            'Authorization HTTP header with JWT refresh token, like: Authorization: Bearer asdf.qwer.zxcv'
        )
    },
    locations=['headers'])
@marshal_with(TokenSchema(only=['access_token']))
@jwt_refresh_token_required
def route_refresh_token():
    user = get_current_user()
    if not user:
        abort(400, 'Could not authenticate user with provided token')
    elif not user.active:
        abort(400, 'Inactive user')
    access_token = create_access_token(identity=user.id)
    print(f'access_token: {access_token}')
    return {'access_token': access_token}


@docs.register
@doc(
    description='Test token access',
    params=authorization_headers,
    tags=['login'])
@app.route(f'{config.API_V1_STR}/login/test-token', methods=['POST'])
@use_kwargs({'test': fields.Str(required=True)})
@marshal_with(UserSchema())
@jwt_required
def route_test_token():
    current_user = get_current_user()
    if current_user:
        return current_user
    else:
        abort(400, 'No user')
    return current_user
