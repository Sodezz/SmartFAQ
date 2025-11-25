from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_starlette import setup_admin
from src.database import engine, get_db
from src.models import Document
from src.schemas.document import SearchRequest, SearchResponse
from src.services.ai_service import AIService

app = FastAPI()

setup_admin(app, engine)


@app.post("/api/ask", response_model=SearchResponse)
async def ask_document(body: SearchRequest, db: AsyncSession = Depends(get_db)):
    ai = AIService()

    query_vector = await ai.get_query_embedding(body.question)

    stmt = (
        select(Document)
        .order_by(Document.embedding.cosine_distance(query_vector))
        .limit(3)
    )
    result = await db.execute(stmt)
    docs = result.scalars().all()

    if not docs:
        return {"answer": "Я не нашел информации в документах."}

    context = "\n\n".join([d.content_document for d in docs if d.content_document])
    answer = await ai.generate_answer(body.question, context)

    return SearchResponse(answer=answer, sources=[d.filename for d in docs])
