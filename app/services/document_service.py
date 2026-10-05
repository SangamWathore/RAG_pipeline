import hashlib
import uuid
from pathlib import Path

from app.repositories.document_repository import DocumentRepository
from app.services.ingestion_service import IngestionService


class DocumentService:

    def __init__(self):
        self.document_dir = Path("documents")

        self.document_dir.mkdir(exist_ok=True)

        self.document_repository = DocumentRepository()
        self.ingestion_service = IngestionService()

    def save_document(
        self,
        filename: str,
        content: bytes,
        uploaded_by: int
    ):
        content_hash = hashlib.sha256(content).hexdigest()

        documents = self.document_repository.get_all()

        existing_document = next(
            (
                document
                for document in documents
                if document.get("content_hash") == content_hash
            ),
            None
        )

        if existing_document:
            raise ValueError("This document already exists")

        document_id = str(uuid.uuid4())

        file_path = (
            self.document_dir
            / f"{document_id}_{filename}"
        )

        file_path.write_bytes(content)

        chunk_count = self.ingestion_service.ingest(
            str(file_path)
        )

        document = {
            "id": document_id,
            "filename": filename,
            "path": str(file_path),
            "chunks": chunk_count,
            "content_hash": content_hash,
            "uploaded_by": uploaded_by
        }

        documents.append(document)

        self.document_repository.save_all(documents)

        return document

    def get_documents(self, uploaded_by: int):
        documents = self.document_repository.get_all()

        return [
            document
            for document in documents
            if document.get("uploaded_by") == uploaded_by
        ]

    def delete_document(
        self,
        document_id: str,
        uploaded_by: int
    ):
        documents = self.document_repository.get_all()

        document = next(
            (
                doc
                for doc in documents
                if doc["id"] == document_id
            ),
            None
        )

        if document is None:
            return None

        if document.get("uploaded_by") != uploaded_by:
            return False

        file_path = Path(document["path"])

        self.ingestion_service.vector_repository.delete_by_source(
            str(file_path)
        )

        if file_path.exists():
            file_path.unlink()

        documents.remove(document)

        self.document_repository.save_all(documents)

        return True