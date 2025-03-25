import requests

from http import HTTPStatus


def test_app_run(app_url):
    response = requests.get(f'{app_url}/status')
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['status'] == 'App is ready'
