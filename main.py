import json
import os
from http import HTTPStatus

from fastapi import FastAPI
from fastapi_pagination import Page, paginate, add_pagination

from models.app import AppStatus
from models.user import User


app = FastAPI()
add_pagination(app)
host = os.getenv('HOST', default='127.0.0.1')
port = os.getenv('APP_PORT', default=8080)


@app.get("/api/users/", response_model=Page[User], status_code=HTTPStatus.OK)
async def get_users() -> Page[User]:
    return paginate(users)


@app.get("/api/users/{user_id}", response_model=User, status_code=HTTPStatus.OK)
async def get_user(user_id: int) -> Page[User]:
    for user in users:
        if user['id'] == user_id:
            return user


@app.get('/status', response_model=AppStatus, status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    return AppStatus(status='App is ready')


if __name__ == "__main__":
    import uvicorn

    with open('users.json') as users_list:
        users = json.load(users_list)

    for user in users:
        User.model_validate(user)

    uvicorn.run(app, host=host, port=port)
