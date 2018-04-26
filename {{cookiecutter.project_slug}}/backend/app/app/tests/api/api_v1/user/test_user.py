import random
import requests

from app.tests.utils.user import random_user, user_authentication_headers
from app.tests.utils.group import get_group_users_and_admins, random_group_admin, random_group
from app.core import config


def test_get_users_superuser_me(server_api, superuser_token_headers):
    r = requests.get(
        f'{server_api}{config.API_V1_STR}/users/me',
        headers=superuser_token_headers)
    current_user = r.json()

    assert current_user['is_active'] == True
    assert current_user['email'] == config.FIRST_SUPERUSER
    assert current_user['is_superuser'] == True


def test_create_user_existing_email(server_api, superuser_token_headers):
    post_data = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=post_data)

    created_user = r.json()

    if r.status_code == 200:
        assert 'id' in created_user
        assert True

    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=post_data)

    created_user = r.json()

    assert r.status_code == 400
    assert 'id' not in created_user


def test_create_user_new_email(server_api, superuser_token_headers):

    post_data = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=post_data)

    created_user = r.json()

    if r.status_code == 200:
        assert 'id' in created_user
        user_id = created_user['id']
        r = requests.get(
            f'{server_api}{config.API_V1_STR}/users/{user_id}',
            headers=superuser_token_headers,
            data=post_data)

        code, response = r.status_code, r.json()

        for key in response:
            assert created_user[key] == response[key]

    if r.status_code == 400:
        assert 'id' not in created_user


def test_user_group_permissions(server_api, superuser_token_headers):

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

        if r.status_code == 200:
            email, password = new_user['email'], new_user['password']
            auth = user_authentication_headers(server_api, email, password)

            allowed_users = group_users[group_id]
            other_users = [
                u for g in group_users for u in group_users[g] if g != group_id
            ]

            for user in allowed_users:
                user_id = user['id']
                r = requests.get(
                    f'{server_api}{config.API_V1_STR}/users/{user_id}',
                    headers=auth)
                assert r.status_code == 200

            for user in other_users:
                user_id = user['id']
                r = requests.get(
                    f'{server_api}{config.API_V1_STR}/users/{user_id}',
                    headers=auth)
                assert r.status_code == 400


def test_create_user_by_superuser(server_api, superuser_token_headers):

    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    expected_fields = [
        "id",
        "is_active",
        "created_at",
        "email",
        "first_name",
        "last_name",
        "group",
        "groups_admin",
        "is_superuser",
    ]

    created_user = r.json()

    for expected_field in expected_fields:
        assert expected_field in created_user

    assert r.status_code == 200


def test_create_user_by_superuser_any_group(server_api,
                                            superuser_token_headers):
    new_group = random_group()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/groups/',
        headers=superuser_token_headers,
        data=new_group)

    created_group = r.json()

    group_id = created_group['id']

    new_user = random_user(group_id)
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    expected_fields = [
        "id",
        "is_active",
        "created_at",
        "email",
        "first_name",
        "last_name",
        "group",
        "groups_admin",
        "is_superuser",
    ]

    created_user = r.json()

    for expected_field in expected_fields:
        assert expected_field in created_user

    assert r.status_code == 200


def test_create_user_by_group_admin(server_api, superuser_token_headers):

    _, group_admin_auth = random_group_admin(server_api,
                                             superuser_token_headers)

    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=group_admin_auth,
        data=new_user)

    assert r.status_code == 400


def test_create_user_by_normal_user(server_api, superuser_token_headers):

    new_user = random_user()
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/users/',
        headers=superuser_token_headers,
        data=new_user)

    created_user = r.json()

    if r.status_code == 200:

        email, password = new_user['email'], new_user['password']
        auth = user_authentication_headers(server_api, email, password)

        new_user = random_user()
        r = requests.post(
            f'{server_api}{config.API_V1_STR}/users/',
            headers=auth,
            data=new_user)

        assert r.status_code == 400