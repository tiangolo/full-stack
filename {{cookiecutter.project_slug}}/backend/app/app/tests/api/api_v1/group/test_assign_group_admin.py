import requests

from app.tests.utils.user import random_user
from app.tests.utils.user import user_authentication_headers

from app.tests.utils.group import random_group
from app.tests.utils.group import random_group_admin

from app.core import config


def test_assign_group_admin_by_superuser(server_api, superuser_token_headers):

    new_group = random_group()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/',
        headers=superuser_token_headers,
        data=new_group)

    created_group = r.json()
    group_id = created_group['id']

    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    created_user = r.json()
    user_id = created_user['id']

    request_data = {"user_id": user_id}

    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/{group_id}/admin_users/',
        headers=superuser_token_headers,
        data=request_data)

    assert r.status_code == 200


def test_assign_group_admin_by_group_admin(server_api,
                                           superuser_token_headers):
    _, group_admin_auth = random_group_admin(server_api,
                                             superuser_token_headers)

    new_group = random_group()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/',
        headers=superuser_token_headers,
        data=new_group)

    created_group = r.json()
    group_id = created_group['id']

    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    created_user = r.json()
    user_id = created_user['id']

    request_data = {"user_id": user_id}

    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/{group_id}/admin_users/',
        headers=group_admin_auth,
        data=request_data)

    assert r.status_code == 400


def test_assign_group_admin_by_normal_user(server_api,
                                           superuser_token_headers):
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
            headers=superuser_token_headers,
            data=new_group)

        created_group = r.json()
        group_id = created_group['id']

        new_user = random_user()
        r = requests.post(
            f'{server_api}{config.API_V1_STR}/users/',
            headers=superuser_token_headers,
            data=new_user)

        created_user = r.json()
        user_id = created_user['id']

        request_data = {"user_id": user_id}

        r = requests.post(
            f'{server_api}{config.API_V1_STR}/groups/{group_id}/admin_users/',
            headers=auth,
            data=request_data)

        assert r.status_code == 400
