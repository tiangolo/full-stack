import requests
import pytest

from app.core import config


@pytest.fixture(scope='module')
def server_api():
    server_name = f'http://{config.SERVER_NAME}'
    return server_name


@pytest.fixture(scope='module')
def superuser_token_headers(server_api):
    login_data = {
        'username': config.FIRST_SUPERUSER,
        'password': config.FIRST_SUPERUSER_PASSWORD
    }
    r = requests.post(
        f'{server_api}{config.API_V1_STR}/login/access-token', data=login_data)
    tokens = r.json()
    a_token = tokens['access_token']
    headers = {'Authorization': f'Bearer {a_token}'}
    return headers
