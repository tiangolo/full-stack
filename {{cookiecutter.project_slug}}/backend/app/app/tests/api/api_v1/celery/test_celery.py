from app.tests.utils.utils import get_server_api
from app.core import config
import requests


def test_celery_worker_test(superuser_token_headers):
    server_api = get_server_api()
    data = {"word": "test"}
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
