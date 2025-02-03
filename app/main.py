from fastapi import FastAPI

from starlette_admin.contrib.sqla import Admin, ModelView

from app.core.database.postgres.database import engine
from app.core.models.postgres.models import DocumentBase
from app.core.models.postgres.router import router as router_documents

app = FastAPI()
admin = Admin(engine, title='Admin panel')

admin.add_view(ModelView(DocumentBase))

admin.mount_to(app)

app.include_router(router_documents)