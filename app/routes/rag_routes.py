from fastapi import APIRouter, Depends, HTTPException, status
from app.services.rag_service import RAGService
from app.schemas.rag_schema import AskRequest, AskResponse
from app.auth.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter()
print("started rag router form main.py import lines 1")
rag_service = None


def get_rag_service():
    """Load the vector store only when the ask endpoint is used."""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service

@router.post("/ask", response_model=AskResponse)
def ask(
        request: AskRequest,
        current_user: User = Depends(get_current_user)):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Question cannot be empty",
        )

    try:
        answer = get_rag_service().ask(question)
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    return {
        "question" : question,
        "answer" : answer["answer"],
        "sources" : answer["sources"],
    }
