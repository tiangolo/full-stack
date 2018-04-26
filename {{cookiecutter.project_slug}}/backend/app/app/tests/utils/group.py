import random

import requests

from app.tests.utils.user import random_user
from app.tests.utils.user import user_authentication_headers
from app.tests.utils.faker import fake

from app.core import config


def random_group():
    return {
        "name": fake.job(),
    }


def random_group_admin(server_api, superuser_token_headers):
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

        return group_id, auth

    else:
        Exception('Unable to execute due to possible server error')


def get_group_users_and_admins(server_api, superuser_token_headers):
    r = requests.get(
        f'{server_api}{config.API_V1_STR}/users/', headers=superuser_token_headers)

    code, response = r.status_code, r.json()
    group_users = {}
    group_admins = []

    for user in response:
        if user['group']:
            group_id = user['group']['id']

            if group_id in group_users:
                group_users[group_id].append(user)
            else:
                group_users[group_id] = [user]

        if user['groups_admin']:
            group_admins.append(user)

    return group_users, group_admins
