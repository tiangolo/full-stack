import requests

from app.tests.utils.user import random_user, user_authentication_headers
from app.tests.utils.group import random_group

from app.core import config


def test_create_group_by_superuser(server_api, superuser_token_headers):

    new_group = random_group()

    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/',
        headers=superuser_token_headers,
        data=new_group)

    expected_fields = ['created_at', 'id', 'name', 'users', 'users_admin']
    created_group = r.json()

    for expected_field in expected_fields:
        assert expected_field in created_group

    assert r.status_code == 200

    assert created_group['users'] == []
    assert created_group['users_admin'] == []
    assert created_group['name'] == new_group['name']


def test_create_group_by_normal_user(server_api, superuser_token_headers):
    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    created_user = r.json()

    if r.status_code == 200:

        email, password = new_user['email'], new_user['password']
        auth = user_authentication_headers(server_api, email, password)

        new_group = random_group()
        r = requests.post(
            f'{server_api}{config.API_V1_STR}/groups/',
            headers=auth,
            data=new_group)

        assert r.status_code == 400
