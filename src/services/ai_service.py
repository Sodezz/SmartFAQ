import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


class AIService:
    def __init__(self):
        self.embedding_model = "models/text-embedding-004"
        self.chat_model = genai.GenerativeModel("gemini-1.5-flash")

    async def create_embedding(self, text: str) -> list[float]:
        result = genai.embed_content(
            model=self.embedding_model, content=text, task_type="retrieval_document"
        )
        return result["embedding"]

    async def get_query_embedding(self, text: str) -> list[float]:
        result = genai.embed_content(
            model=self.embedding_model, content=text, task_type="retrieval_query"
        )
        return result["embedding"]

    async def generate_answer(self, query: str, context_docs: str) -> str:

        context_text = "\n\n".join(context_docs)

        prompt = f"""
        Ты умный помощник. Используй только следующую информацию для ответа на вопрос пользователя.
        Если информации недостаточно, скажи "Я не знаю ответа на основе предоставленных документов".

        Контекст:
        {context_text}

        Вопрос пользователя:
        {query}
        """

        response = await self.chat_model.generate_content_async(prompt)
        return response.text
