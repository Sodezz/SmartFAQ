# AI Document Search Service

Сервис на базе FastAPI для загрузки документов и интеллектуального поиска по ним с использованием векторного представления (Embeddings) и Google Gemini API. Реализует подход RAG (Retrieval Augmented Generation).

## Стек технологий

*   **Язык:** Python 3.11+
*   **Веб-фреймворк:** FastAPI
*   **База данных:** PostgreSQL 16 + pgvector 
*   **ORM:** SQLAlchemy (Async)
*   **Миграции:** Alembic
*   **Админ-панель:** Starlette Admin
*   **AI/LLM:** Google Generative AI (Gemini 1.5 Flash, text-embedding-004)
*   **Управление зависимостями:** uv
*   **Контейнеризация:** Docker, Docker Compose

## Функциональность

1.  **Административная панель:** Интерфейс для управления пользователями и загрузки документов (PDF, TXT).
2.  **Векторизация:** При загрузке документа его текст автоматически преобразуется в вектор (embeddings) и сохраняется в базу данных.
3.  **Семантический поиск:** API принимает вопрос пользователя, находит наиболее релевантные фрагменты документов с помощью косинусного сходства.
4.  **Генерация ответа:** Найденный контекст передается в LLM для формирования ответа на естественном языке.

## Требования

*   Docker и Docker Compose
*   Ключ API от Google AI Studio (Google Gemini)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd <ИМЯ_ПАПКИ>
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта. Вы можете скопировать пример ниже:

```ini
# Настройки базы данных для Docker
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=my_database
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Строка подключения для SQLAlchemy (внутри Docker контейнера)
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/my_database

# Ключ API Google (получить в AI Studio)
GOOGLE_API_KEY=ваш_ключ_здесь
```

### 3. Запуск через Docker (Рекомендуемый способ)

Сборка и запуск контейнеров:

```bash
docker-compose up --build -d
```

При первом запуске необходимо применить миграции базы данных. Выполните команду внутри контейнера приложения:

```bash
docker-compose exec app alembic upgrade head
```

Сервис будет доступен по адресу: `http://localhost:8000`

### 4. Локальная разработка (без Docker-контейнера приложения)

Если вы хотите запустить приложение локально, но базу данных оставить в Docker:

1.  Установите менеджер пакетов `uv`.
2.  Запустите только базу данных:
    ```bash
    docker-compose up -d db
    ```
3.  Измените `DATABASE_URL` в `.env` на localhost:
    ```ini
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/my_database
    ```
4.  Установите зависимости и запустите проект:
    ```bash
    uv sync
    uv run alembic upgrade head
    uv run uvicorn src.main:app --reload
    ```

## Использование

### Админ-панель

Доступна по адресу: `http://localhost:8000/admin`

1.  Зайдите в раздел **Documents**.
2.  Нажмите **Create**.
3.  Загрузите файл (поддерживаются `.txt` и `.pdf`).
4.  Система автоматически извлечет текст и создаст векторное представление.

### API Поиска

**Эндпоинт:** `POST /api/ask`

**Пример запроса:**

```json
{
  "question": "Как настроить этот проект?"
}
```

**Пример ответа:**

```json
{
  "answer": "Для настройки проекта необходимо создать файл .env и запустить docker-compose up.",
  "sources": [
    "readme.txt",
    "manual.pdf"
  ]
}
```

### Документация API

Интерактивная документация Swagger UI доступна по адресу:
`http://localhost:8000/docs`

## Структура проекта

*   `alembic/` - Файлы миграций базы данных.
*   `src/` - Исходный код приложения.
    *   `core/` - Конфигурация и зависимости.
    *   `schemas/` - Pydantic схемы для валидации данных.
    *   `services/` - Бизнес-логика (работа с AI).
    *   `admin_starlette.py` - Настройка админ-панели.
    *   `database.py` - Подключение к БД.
    *   `main.py` - Точка входа FastAPI.
    *   `models.py` - SQLAlchemy модели.
*   `uploads/` - Директория для хранения загруженных файлов.
*   `docker-compose.yml` - Конфигурация Docker сервисов.
*   `pyproject.toml` - Список зависимостей и настройки uv.
