from fastapi import APIRouter, Depends
from app.services.rag_service import RAGService
from app.schemas.rag_schema import AskResponse
from app.auth.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter()
print("started rag router form main.py import lines 1")
rag_service = RAGService()

@router.get("/ask",response_model=AskResponse)
def ask(question:str, 
        current_user: User = Depends(get_current_user)):
    answer = rag_service.ask(question)

    return {
        "question" : question,
        "answer" : answer
    }
