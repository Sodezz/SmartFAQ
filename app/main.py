from fastapi import FastAPI

from app.routes import documents, users

app = FastAPI()

app.include_router(users.router)
app.include_router(documents.router)
