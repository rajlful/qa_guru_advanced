import os

import dotenv
import pytest


@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope='session')
def app_url() -> str:
    return f'{os.getenv("APP_URL")}/{{os.getenv("APP_PORT")}}'


@pytest.fixture(scope='session')
def users_endpoint() -> str:
    app_url = os.getenv("APP_URL")
    return f'{app_url}/api/users'
