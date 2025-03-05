from starlette_admin.contrib.sqla import Admin, ModelView

from core.models.postgres.models import FAQ, DocumentBase
from core.database.postgres.database import engine
from main import app


class FAQView(ModelView):
    model = FAQ
    name = "FAQ"
    list_display = ["id", "question", "answer"]

class DocumentView(ModelView):
    model = DocumentBase
    name = "Documents"
    list_display = ["id", "uploaded_by", "store_doc"]
    form_display = ["uploaded_by", "store_doc"] # Форма загрузки документа

admin = Admin(engine, title="Admin panel")
admin.add_view(FAQView(FAQ))
admin.mount_to(app)