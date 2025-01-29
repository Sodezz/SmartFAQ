import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

Base = declarative_base()

load_dotenv()

database_url = (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT_OUT')}/{os.getenv('POSTGRES_DB')}"
                )

engine = create_engine(database_url)
session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_database():
    database = session()
    try:
        yield database
    finally:
        database.close()