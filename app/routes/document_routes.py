from fastapi import UploadFile,HTTPException,File,APIRouter
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentUploadResponse,DocumentListResponse


router = APIRouter(prefix="/documents",
                   tags=["Documents"]
                   )
print("started document router form main.py import lines 3")
document_service = DocumentService()


#this code will not exectute until the user is clicked on upload api
@router.post("/upload",response_model=DocumentUploadResponse)
async def upload_document(
    file:UploadFile=File(...)
):
    print("uploading document 6")
    content = await file.read()

    document = document_service.save_document(
        filename=file.filename,
        content=content
    )

    return {
        "message" : "Document uploaded successfully",
        "document" : document
    }

@router.get("/", response_model=DocumentListResponse)
def get_documents():

    documents = document_service.get_document()

    return {
        "documents" : documents
    }

@router.delete("/{document_id}")
def delete_document(document_id:str):
    deleted = document_service.delete_document(
        document_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    return {
        "message":"Document Deleted succussfully"
    }