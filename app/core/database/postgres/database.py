import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

engine = create_engine(database_url)
session = sessionmaker(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()