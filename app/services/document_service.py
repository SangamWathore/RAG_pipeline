import json
import uuid
from pathlib import Path
from app.services.ingestion_service import IngestionService
from app.repositories.document_repository import DocumentRepository

class DocumentService:
    def __init__(self):
        self.document_dir = Path("documents")

        print(" DocumentService class initialized 4")   
        
        self.document_dir.mkdir(exist_ok=True)

        self.document_repository = DocumentRepository()

        self.ingestion_service = IngestionService()
    

    def save_document(self,filename:str,content:bytes):
        document_id = str(uuid.uuid4())
        file_path = self.document_dir / f"{document_id}_{filename}"
        file_path.write_bytes(content)
        
        print("Document saved at 7")

        #ingest document into vectorstore
        chunk_count = self.ingestion_service.ingest(
            str(file_path)
        )

        documents = self.document_repository.get_all()

        document = {
            "id":document_id,
            "filename":filename,
            "path":str(file_path),
            "chunks":chunk_count
        }
        documents.append(document)
        self.document_repository.save_all(documents)

        return document

    def get_document(self):
        return self.document_repository.get_all()
    
    def delete_document(self,document_id:str):
        
        documents = self.document_repository.get_all()
        document = next(
            (doc 
            for doc in documents
            if doc["id"] == document_id
            ),
            None
        )
        if document is None:
            return False

        file_path = Path(documents["path"])

        if file_path.exists():
            file_path.unlink()

        documents.remove(document)

        self.document_repository.save_all(documents)

        return True
        