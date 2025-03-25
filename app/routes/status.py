from http import HTTPStatus

from fastapi import APIRouter

from app.database.engine import check_db_is_ready
from app.models.app import AppStatus


router = APIRouter()


@router.get('/status', response_model=AppStatus, status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    if check_db_is_ready():
        return AppStatus(status='App is ready')
    else:
        return AppStatus(status='DB is not available')
