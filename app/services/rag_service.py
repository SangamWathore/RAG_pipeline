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
            f"[Source {index}]\n{doc.page_content}"
            for index, doc in enumerate(relevant_documents, start=1)
        )

        prompt = f"""
Answer the question using only the context below.
When referring to information, cite the source number in square brackets,
for example [Source 1]. If the answer is not supported by the context, say so.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        sources = []
        for doc in relevant_documents:
            metadata = doc.metadata or {}
            sources.append({
                "source": metadata.get("source") or metadata.get("filename"),
                "page": metadata.get("page"),
                "content": doc.page_content[:500],
            })

        return {"answer": response.content, "sources": sources}
