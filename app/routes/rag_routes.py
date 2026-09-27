from fastapi import APIRouter
from app.services.rag_service import RAGService
from app.schemas.rag_schema import AskResponse

router = APIRouter()
print("started rag router form main.py import lines 1")
rag_service = RAGService()

@router.get("/ask",response_model=AskResponse)
def ask(question:str):
    answer = rag_service.ask(question)

    return {
        "question" : question,
        "answer" : answer
    }
