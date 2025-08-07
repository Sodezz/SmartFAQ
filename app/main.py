import os
import io
import re
import uuid
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .vector_store import SimpleVectorStore
from .text_extraction import extract_text_from_file
from .qa import generate_answer

APP_DATA_DIR = os.environ.get("APP_DATA_DIR", "/workspace/app_data")
UPLOADS_DIR = os.path.join(APP_DATA_DIR, "uploads")
INDEX_DIR = os.path.join(APP_DATA_DIR, "index")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

app = FastAPI(title="Document QA API", version="1.0.0")


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    max_context_chars: int = 3000


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]


# Initialize vector store
vector_store = SimpleVectorStore(INDEX_DIR)
vector_store.load()


def split_text_into_chunks(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> List[str]:
    if not text:
        return []
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        # Try to break on the last sentence boundary within the window
        window = text[start:end]
        last_boundary = max(window.rfind(". "), window.rfind("? "), window.rfind("! "))
        if last_boundary != -1 and (start + last_boundary + 1 - start) >= chunk_size * 0.5:
            end = start + last_boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - chunk_overlap, 0)
        if start >= len(text):
            break
    return chunks


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/documents")
async def upload_documents(files: List[UploadFile] = File(...)) -> JSONResponse:
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    added_chunks = 0
    added_files: List[Dict[str, Any]] = []

    for f in files:
        filename = f.filename or f"upload-{uuid.uuid4()}"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in {".pdf", ".docx"}:
            raise HTTPException(status_code=415, detail=f"Unsupported file type: {ext}. Supported: .pdf, .docx")

        # Persist file
        target_path = os.path.join(UPLOADS_DIR, filename)
        with open(target_path, "wb") as out:
            out.write(await f.read())

        # Extract text
        try:
            text, meta = extract_text_from_file(target_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text from {filename}: {e}")

        chunks = split_text_into_chunks(text)
        metas = [{
            "source_file": filename,
            "source_path": target_path,
            **({"page_ranges": meta.get("page_ranges")} if meta and meta.get("page_ranges") else {})
        } for _ in chunks]

        if chunks:
            vector_store.add_texts(chunks, metas)
            added_chunks += len(chunks)
            added_files.append({"filename": filename, "chunks": len(chunks)})

    vector_store.save()

    return JSONResponse({
        "status": "indexed",
        "files": added_files,
        "total_chunks": added_chunks,
        "corpus_size": vector_store.size()
    })


@app.post("/query", response_model=QueryResponse)
async def query_documents(payload: QueryRequest) -> QueryResponse:
    if vector_store.size() == 0:
        raise HTTPException(status_code=400, detail="No documents indexed yet")

    results = vector_store.query(payload.question, top_k=max(1, min(payload.top_k, 20)))

    # Build context for optional LLM answer
    context_parts = [r["text"] for r in results]
    context = "\n\n".join(context_parts)
    if len(context) > payload.max_context_chars:
        context = context[: payload.max_context_chars]

    answer_text = await generate_answer(question=payload.question, context=context)

    sources_out = [
        {
            "score": r["score"],
            "text": r["text"],
            "metadata": r["metadata"],
        }
        for r in results
    ]

    return QueryResponse(answer=answer_text, sources=sources_out)


@app.delete("/reset")
async def reset_index() -> Dict[str, Any]:
    vector_store.reset()
    return {"status": "reset"}
