import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
POSTGRES_PORT=os.getenv('POSTGRES_PORT_OUT')
POSTGRES_DB=os.getenv('POSTGRES_DB')

database_url = (f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
                f"{POSTGRES_PORT}/{POSTGRES_DB}"
                )

engine = create_async_engine(database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

def get_database():
    database = async_session()
    try:
        yield database
    finally:
        database.close()