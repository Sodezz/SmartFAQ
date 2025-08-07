import os
from typing import Tuple, Dict, Any

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(path: str) -> Tuple[str, Dict[str, Any]]:
    reader = PdfReader(path)
    texts = []
    page_ranges = []
    for i, page in enumerate(reader.pages):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt.strip():
            texts.append(txt)
            page_ranges.append(i + 1)
    return "\n\n".join(texts), {"page_ranges": page_ranges}


def extract_text_from_docx(path: str) -> Tuple[str, Dict[str, Any]]:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(paragraphs), {}


def extract_text_from_file(path: str) -> Tuple[str, Dict[str, Any]]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    if ext == ".docx":
        return extract_text_from_docx(path)
    raise ValueError(f"Unsupported file type: {ext}")