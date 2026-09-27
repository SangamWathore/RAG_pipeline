from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.repositories.vector_repository import VectorRepository


class IngestionService:

    def __init__(self):

        self.vector_repository = VectorRepository()

    def ingest(self, file_path: str):

        # 1. Load document
        loader = TextLoader(file_path)

        documents = loader.load()

        # 2. Split document
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=10
        )

        chunks = splitter.split_documents(
            documents
        )

        # 3. Create or update vectorstore
        if self.vector_repository.exists():

            self.vector_repository.load()

            self.vector_repository.add_documents(
                chunks
            )

        else:

            self.vector_repository.create(
                chunks
            )

        # 4. Save vectorstore
        self.vector_repository.save()

        return len(chunks)