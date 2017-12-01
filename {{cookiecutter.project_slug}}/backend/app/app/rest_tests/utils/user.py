import requests

from .faker import fake

from app.core import config


def random_user(group_id=1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    app_id = f'{first_name}.{last_name}'
    fake_user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'app_id': app_id,
        'group_id': group_id,
        'password': 'pstest'
    }
    return fake_user


def user_authentication_headers(server_api, email, password):
    data = {"email": email, "password": password}

    r = requests.post(f'{server_api}{config.API_V1_STR}/login/', data=data)

    response = r.json()
    auth_token = response['access_token']
    headers = {'Authorization': f'Bearer {auth_token}'}
    return headers