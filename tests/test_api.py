import json
from http import HTTPStatus

import pytest
import random
import requests
from app.models.user import User
from app.database import users as users_db
from tests.test_data.users_data import fake_user


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture(scope="module", autouse=True)
def fill_db(app_url):
    with open(rf'C:\Users\rajl\Desktop\qa_guru_advanced\app\routes\users.json') as f:
        users = json.load(f)
    api_users = []
    for user in users:
        res = requests.post(f'{app_url}/api/users', json=user)
        api_users.append(res.json())
    user_ids = [user["id"] for user in api_users]
    yield user_ids
    for user_id in user_ids:
        requests.delete(f'{app_url}/api/users/{user_id}')


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    for user in response.json()['items']:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users['items']]
    assert len(users_ids) == len(set(users_ids))


def test_user(app_url, fill_db):
    user_id = random.randint(1, len(fill_db))
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    User.model_validate(user)


def test_user_nonexistent_values(app_url, fill_db):
    user_id = max(fill_db) + 1
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, 1.4, "kek"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(app_url):
    new_user = requests.post(f"{app_url}/api/users/", json=fake_user()).json()
    users = users_db.get_users()
    user_id = None
    for user in users:
        if (user.email == new_user['email'] and
                user.first_name == new_user['first_name'] and
                user.last_name == new_user['last_name'] and
                user.avatar == new_user['avatar']):
            user_id = user.id
    assert users_db.get_user(user_id)


def test_delete_user(app_url):
    new_user = requests.post(f"{app_url}/api/users/", json=fake_user()).json()
    users = users_db.get_users()
    user_id = None
    for user in users:
        if (user.email == new_user['email'] and
                user.first_name == new_user['first_name'] and
                user.last_name == new_user['last_name'] and
                user.avatar == new_user['avatar']):
            user_id = user.id
    assert users_db.get_user(user_id)
    users_db.delete_user(user_id)
    assert not users_db.get_user(user_id)


def test_update_user(app_url, fill_db):
    user_id = random.randint(1, len(fill_db))
    update_model = fake_user()
    user_before_update = users_db.get_user(user_id)
    requests.patch(f"{app_url}/api/users/{user_id}", json=update_model).json()
    user_after_update = users_db.get_user(user_id)
    assert user_before_update.email != user_after_update.email
    assert user_before_update.last_name != user_after_update.last_name
    assert user_before_update.first_name != user_after_update.first_name
    assert user_before_update.avatar != user_after_update.avatar
