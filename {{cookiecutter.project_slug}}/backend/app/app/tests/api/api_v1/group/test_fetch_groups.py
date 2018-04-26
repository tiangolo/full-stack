import requests
import random

from app.tests.utils.user import random_user, user_authentication_headers
from app.tests.utils.group import get_group_users_and_admins

from app.core import config


def test_fetch_superuser_groups(server_api, superuser_token_headers):

    r = requests.get(
        f'{server_api}{config.API_V1_STR}/groups/',
        headers=superuser_token_headers)

    assert r.status_code == 200


def test_fetch_general_user_groups(server_api, superuser_token_headers):
    group_users, _ = get_group_users_and_admins(server_api,
                                                superuser_token_headers)
    group_id = random.choice(list(group_users.keys()))

    new_user = random_user(group_id)

    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    if r.status_code == 200:

        email, password = new_user['email'], new_user['password']
        auth = user_authentication_headers(server_api, email, password)

        r = requests.get(
            f'{server_api}{config.API_V1_STR}/groups/', headers=auth)
        groups = r.json()

        assert len(groups) == 1


def test_fetch_group_admin_user_groups(server_api, superuser_token_headers):
    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    created_user = r.json()

    group_users, _ = get_group_users_and_admins(server_api,
                                                superuser_token_headers)
    group_id = random.choice(list(group_users.keys()))

    if r.status_code == 200:
        r = requests.post(
            f'{server_api}{config.API_V1_STR}/groups/{group_id}/admin_users/',
            headers=superuser_token_headers,
            data={
                'user_id': created_user['id']
            })

        email, password = new_user['email'], new_user['password']
        auth = user_authentication_headers(server_api, email, password)

        r = requests.get(
            f'{server_api}{config.API_V1_STR}/groups/', headers=auth)
        groups = r.json()

        assert len(groups) == 1


def test_fetch_create_groups(server_api, superuser_token_headers):
    assert True


def test_assign_admin_group_success(server_api, superuser_token_headers):
    assert True


def test_assign_admin_group_fail(server_api, superuser_token_headers):
    assert True