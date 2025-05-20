import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.core.models.models as models

# Загружаем переменные окружения из .env
load_dotenv()

# Чтение параметров подключения из окружения
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT_OUT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Формируем URL подключение к БД
database_url = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Создаём SQLAlchemy Engine — для соединений с БД
engine = create_engine(database_url)

sessionLocal = sessionmaker(bind=engine)

# Создаём все таблицы в базе данных на основе моделей, если они ещё не созданы
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Зависимость FastAPI для получения сессии БД.

    При каждом вызове создаёт новую сессию, отдаёт её в роуты,
    а после завершения работы автоматически закрывает.
    """
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
