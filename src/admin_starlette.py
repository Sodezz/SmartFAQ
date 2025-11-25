import os

import aiofiles
from pypdf import PdfReader
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin, ModelView

from src.database import engine
from src.models import Document, User
from src.services.ai_service import AIService

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentView(ModelView):
    exclude_fields_from_create = ["embedding", "content_document"]
    exclude_fields_from_edit = ["embedding", "content_document"]

    async def create(self, request: Request, data: dict) -> any:

        file: UploadFile = data.get("filename")

        if not file:
            return await super().create(request, data)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        data["filename"] = file.filename

        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        text_content = ""
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text_content += page.extract_text() or ""
        else:

            text_content = content.decode("utf-8", errors="ignore")

        ai = AIService()
        try:

            embedding = await ai.get_query_embedding(text_content[:8000])
        except Exception as e:
            print(f"Error AI: {e}")
            embedding = None

        data["content_document"] = text_content
        data["embedding"] = embedding

        return await super().create(request, data)


def setup_admin(app, db_engine):
    admin = Admin(engine, title="My AI Docs")
    admin.add_view(ModelView(User))
    admin.add_view(DocumentView(Document))
    admin.mount_to(app)
