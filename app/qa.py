import os
from typing import Optional

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


async def generate_answer(question: str, context: str) -> str:
    if OPENAI_API_KEY:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            system_prompt = (
                "You are a helpful assistant. Answer the user's question strictly based on the provided context. "
                "If the answer is not in the context, say you don't know. Keep it concise."
            )
            prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
            resp = await client.responses.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_output_tokens=256,
            )
            text = resp.output_text  # type: ignore[attr-defined]
            return text.strip()
        except Exception:
            pass
    # Fallback: return the most relevant context snippet directly
    if not context.strip():
        return "Я не нашёл ответа в загруженных документах."
    # Return first 500 chars as a concise extract
    snippet = context.strip().split("\n\n")[0]
    return snippet[:500]