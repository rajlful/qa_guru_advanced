import os

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.database.engine import create_db_tables
from routes import status, users

host = os.getenv('HOST', default='127.0.0.1')
port = os.getenv('APP_PORT', default=8080)

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)


if __name__ == "__main__":
    import uvicorn
    create_db_tables()
    print(f'kek {type(port)}')
    uvicorn.run(app=app, host=host, port=port)
