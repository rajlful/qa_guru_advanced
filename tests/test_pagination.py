import math
from http import HTTPStatus

import pytest
import requests


@pytest.fixture(scope='module')
def users_count(users_endpoint) -> int:
    response = requests.get(users_endpoint)
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    return body['total']


@pytest.mark.parametrize('size', (1, 3, 5))
def test_count_users_on_page_by_size_change(users_endpoint, size):
    response = requests.get(f'{users_endpoint}', params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    items = body['items']
    assert len(items) == size


@pytest.mark.parametrize('size', (1, 6, 12, 100))
def test_count_page_by_size_change(users_endpoint, users_count, size):
    response = requests.get(f'{users_endpoint}', params={'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    actual_pages = body['pages']
    expected_pages = math.ceil(users_count / size)

    assert actual_pages == expected_pages
    assert body['page'] == 1
    assert body['size'] == size
    assert body['total']


def test_results_items_by_page_change(users_endpoint):
    size = 4
    page_one = requests.get(users_endpoint, params={'page': 1, 'size': size})
    assert page_one.status_code == HTTPStatus.OK
    body_one = page_one.json()
    page_two = requests.get(users_endpoint, params={'page': 2, 'size': size})
    assert page_two.status_code == HTTPStatus.OK
    body_two = page_two.json()
    assert body_one['page'] != body_two['page']
    assert body_one['size'] == body_two['size'] == size
