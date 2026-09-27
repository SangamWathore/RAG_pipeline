from langchain_openai import ChatOpenAI

from app.config import LLM_MODEL
from app.repositories.vector_repository import VectorRepository


class RAGService:

    def __init__(self):

        self.vector_repository = VectorRepository()

        self.vector_repository.load()

        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0
        )

    def ask(self, question: str):

        relevant_documents = self.vector_repository.search(
            question,
            k=2
        )

        context = "\n\n".join(
            doc.page_content
            for doc in relevant_documents
        )

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content