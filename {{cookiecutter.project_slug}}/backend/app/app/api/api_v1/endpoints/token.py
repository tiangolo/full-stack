# Import standard library
from datetime import timedelta

# Import installed modules
from flask import abort
from flask_apispec import doc, use_kwargs, marshal_with
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from webargs import fields

# Import app code
from ..api_docs import docs, security_params
from app.core import config
from app.core.security import pwd_context, verify_password
from app.db.flask_session import db_session
from app.db.utils import get_user_by_username, get_user_hashed_password, get_user_id
from app.main import app

# Import Schemas
from app.schemas.token import TokenSchema
from app.schemas.user import UserSchema

# Import models
from app.models.user import User


@docs.register
@doc(
    description="OAuth2 compatible token login, get an access token for future requests",
    tags=["login"],
)
@app.route(f"{config.API_V1_STR}/login/access-token", methods=["POST"])
@use_kwargs(
    {"username": fields.Str(required=True), "password": fields.Str(required=True)}
)
@marshal_with(TokenSchema())
def route_login_access_token(username, password):
    user = get_user_by_username(username, db_session)

    if not user or not verify_password(password, get_user_hashed_password(user)):
        abort(400, "Incorrect email or password")
    elif not user.is_active:
        abort(400, "Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            identity=get_user_id(user), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@docs.register
@doc(description="Test access token", tags=["login"], security=security_params)
@app.route(f"{config.API_V1_STR}/login/test-token", methods=["POST"])
@use_kwargs({"test": fields.Str(required=True)})
@marshal_with(UserSchema())
@jwt_required
def route_test_token(test):
    current_user = get_current_user()
    if current_user:
        return current_user
    else:
        abort(400, "No user")
    return current_user


@docs.register
@doc(
    description='Test access token manually, same as the endpoint to "Test access token" but copying and adding the Authorization: Bearer <token>',
    params={
        "Authorization": {
            "description": "Authorization HTTP header with JWT token, like: Authorization: Bearer asdf.qwer.zxcv",
            "in": "header",
            "type": "string",
            "required": True,
        }
    },
    tags=["login"],
)
@app.route(f"{config.API_V1_STR}/login/manual-test-token", methods=["POST"])
@use_kwargs({"test": fields.Str(required=True)})
@marshal_with(UserSchema())
@jwt_required
def route_manual_test_token(test):
    current_user = get_current_user()
    if current_user:
        return current_user
    else:
        abort(400, "No user")
    return current_user
