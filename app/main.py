import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.database.engine import create_db_tables
from app.routes import status, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('On start up')
    create_db_tables()
    yield
    logging.info('On shut down')


host = os.getenv('HOST', default='127.0.0.1')
port = os.getenv('APP_PORT', default=8080)

app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host=host, port=port)
