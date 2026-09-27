from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.config import EMBEDDING_MODEL


class VectorRepository:

    def __init__(self):

        self.vectorstore_path = "vectorstore"

        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL
        )

        self.vectorstore = None

    def exists(self):

        index_file = Path(
            self.vectorstore_path,
            "index.faiss"
        )

        return index_file.exists()

    def load(self):

        self.vectorstore = FAISS.load_local(
            self.vectorstore_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def create(self, documents):

        self.vectorstore = FAISS.from_documents(
            documents,
            embedding=self.embeddings
        )

    def add_documents(self, documents):

        self.vectorstore.add_documents(
            documents
        )

    def save(self):

        self.vectorstore.save_local(
            self.vectorstore_path
        )

    def search(self, query, k=2):

        return self.vectorstore.similarity_search(
            query,
            k=k
        )