from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declared_attr

database_url =  "postgresql+psycopg2://postgres:5623@DataBase:5432/postgres"

engine = create_engine(database_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    database = session()
    try:
        yield database
    finally:
        database.close()