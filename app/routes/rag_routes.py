from fastapi import APIRouter, Depends, HTTPException, status
from app.services.rag_service import RAGService
from app.schemas.rag_schema import AskRequest, AskResponse
from app.auth.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter()
print("started rag router form main.py import lines 1")
rag_service = RAGService()

@router.post("/ask", response_model=AskResponse)
def ask(
        request: AskRequest,
        current_user: User = Depends(get_current_user)):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Question cannot be empty",
        )

    answer = rag_service.ask(question)

    return {
        "question" : question,
        "answer" : answer["answer"],
        "sources" : answer["sources"],
    }
