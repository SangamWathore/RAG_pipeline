# python -m app.rebuild_vectorstore

from app.services.ingestion_service import IngestionService

ingestion_service = IngestionService()

chunk_count = ingestion_service.ingest("company.txt")

print(f"Vectorstore recreated successfully.")
print(f"Chunks created: {chunk_count}")