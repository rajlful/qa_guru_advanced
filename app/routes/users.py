import json
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate


from app.models.user import User, UserUpdate, UserCreate
from app.database import users

router = APIRouter(prefix='/api/users')


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
async def get_users() -> Page[User]:
    return paginate(users.get_users())


@router.get("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
async def get_user(user_id: int) -> Page[User]:
    if user_id < 1 or not user_id.is_integer():
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
async def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
async def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return {"message": "User deleted"}
