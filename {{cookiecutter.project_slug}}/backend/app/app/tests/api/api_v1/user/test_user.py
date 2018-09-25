import random
import requests

from app.db.external_session import db_session
from app.db.utils import get_user_by_username, create_user

from app.tests.utils.utils import get_server_api, random_lower_string
from app.tests.utils.user import user_authentication_headers
from app.core import config


def test_get_users_superuser_me(superuser_token_headers):
    server_api = get_server_api()
    r = requests.get(
        f"{server_api}{config.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()

    assert current_user["is_active"] is True
    assert current_user["email"] == config.FIRST_SUPERUSER
    assert current_user["is_superuser"] is True

def test_create_user_new_email(superuser_token_headers):
    server_api = get_server_api()
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = get_user_by_username(username, db_session)
    assert user.email == username
    assert user.is_active is True


def test_create_user_existing_username(superuser_token_headers):
    server_api = get_server_api()
    username = random_lower_string()
    password = random_lower_string()
    user = create_user(db_session, username, password)
    data = {"email": username, "password": password}
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "id" not in created_user


def test_create_user_by_normal_user(superuser_token_headers):
    server_api = get_server_api()

    username = random_lower_string()
    password = random_lower_string()
    user = create_user(db_session, username, password)
    auth = user_authentication_headers(server_api, username, password)

    username2 = random_lower_string()
    password2 = random_lower_string()
    data = {"email": username2, "password": password2}
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/users/", headers=auth, data=data
    )
    assert r.status_code == 400
