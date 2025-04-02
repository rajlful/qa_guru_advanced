import dotenv
import os

from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

dotenv.load_dotenv()

engine = create_engine(
    os.getenv('DATABASE_ENGINE', default='postgresql://postgres:Admin12345!@db:5432/postgres'),
    pool_size=10
)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def check_db_is_ready() -> bool:
    try:
        with Session(engine) as s:
            s.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f'{e} was occurred. Db is unvailable')
        return True
