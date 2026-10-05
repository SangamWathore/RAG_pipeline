from fastapi import UploadFile,HTTPException,File,APIRouter, Depends
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentUploadResponse,DocumentListResponse
from app.models.user_model import User
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/documents",tags=["Documents"])


document_service = DocumentService()


#this code will not exectute until the user is clicked on upload api
@router.post("/upload",response_model=DocumentUploadResponse)

async def upload_document(    
    file:UploadFile=File(...),
    current_user = Depends(get_current_user)
):
    
    content = await file.read()

    try:
        document = document_service.save_document(
            filename=file.filename,
            content=content,
            uploaded_by=current_user.id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    return {
        "message" : "Document uploaded successfully",
        "document" : document
    }

@router.get("/", response_model=DocumentListResponse)
def get_documents(
    current_user: User = Depends(get_current_user)
    ):

    documents = document_service.get_documents(
        uploaded_by=current_user.id
    )
    

    return {
        "documents" : documents
    }

@router.delete("/{document_id}")
def delete_document(document_id:str,
                    current_user: User = Depends(get_current_user)
    ):
    
    deleted = document_service.delete_document(
        document_id=document_id,
        uploaded_by=current_user.id
    )
    
    if deleted is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

    if deleted is False:
                raise HTTPException(
                    status_code=403,
                    detail="You cannot delete another user's document"
                )
    
    return {
        "message": "Document deleted successfully"
    }